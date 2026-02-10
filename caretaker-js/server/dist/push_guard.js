import { GitHub } from './github';
import { logger } from './logger';
import { config } from './config';
import { execa } from 'execa';
import fs from 'fs';
import path from 'path';
export async function ensureBranchProtection(gh, owner, repo) {
    const url = `${config.githubRest}/repos/${owner}/${repo}/branches/main/protection`;
    const res = await fetch(url, {
        method: 'PUT', headers: { Authorization: `Bearer ${config.token}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ required_pull_request_reviews: { required_approving_review_count: 2 }, required_status_checks: { strict: true, contexts: ['build', 'test', 'security-audit'] } })
    });
    if (!res.ok)
        logger.warn({ status: res.status }, 'branch protection update failed');
}
async function runChecks(cwd) {
    const log = {};
    if (fs.existsSync(path.join(cwd, 'package.json'))) {
        try {
            await execa('npm', ['ci'], { cwd });
            log.npm_ci = 'ok';
        }
        catch (e) {
            log.npm_ci = e.message;
            throw e;
        }
        try {
            await execa('npm', ['test', '--silent'], { cwd });
            log.tests = 'ok';
        }
        catch (e) {
            log.tests = e.message;
            throw e;
        }
        try {
            await execa('npm', ['run', 'build', '--silent'], { cwd });
            log.build = 'ok';
        }
        catch (e) {
            log.build = e.message;
            throw e;
        }
        try {
            const r = await execa('npm', ['audit', '--json'], { cwd });
            log.audit = JSON.parse(r.stdout);
        }
        catch (e) {
            log.audit = e.stdout || e.message;
        }
    }
    return log;
}
export async function securePushFlow(repoUrl, branch = 'main') {
    const tmp = fs.mkdtempSync(path.join(process.cwd(), 'push-'));
    const tokenRepo = repoUrl.replace('https://', 'https://' + config.token + '@');
    await execa('git', ['clone', tokenRepo, tmp]);
    const checks = await runChecks(tmp);
    const auditDir = path.join(process.cwd(), 'logs');
    fs.mkdirSync(auditDir, { recursive: true });
    const logPath = path.join(auditDir, `secure-push-${Date.now()}.json`);
    fs.writeFileSync(logPath, JSON.stringify({ repoUrl, branch, checks }, null, 2));
    const backupTag = `backup/${branch}/${Date.now()}`;
    await execa('git', ['-C', tmp, 'fetch', 'origin', branch]);
    await execa('git', ['-C', tmp, 'tag', backupTag, `origin/${branch}`]);
    await execa('git', ['-C', tmp, 'push', 'origin', backupTag]);
    const feature = `caretaker/push-${Date.now()}`;
    await execa('git', ['-C', tmp, 'checkout', '-b', feature]);
    await execa('git', ['-C', tmp, 'push', 'origin', feature]);
    const [owner, name] = repoUrl.split('/').slice(-2);
    const gh = new GitHub(config.token);
    await ensureBranchProtection(gh, owner.split(':').pop().replace('.git', ''), name.replace('.git', ''));
    await fetch(`${config.githubRest}/repos/${owner}/${name}/pulls`, { method: 'POST', headers: { Authorization: `Bearer ${config.token}`, 'Content-Type': 'application/json' }, body: JSON.stringify({ title: 'Secure Push Validation', head: feature, base: branch, body: 'Automated validation PR created by CareTaker.' }) });
    return { ok: true, logPath };
}
export async function rollback(repoUrl, tag) {
    const tmp = fs.mkdtempSync(path.join(process.cwd(), 'rollback-'));
    const tokenRepo = repoUrl.replace('https://', 'https://' + config.token + '@');
    await execa('git', ['clone', tokenRepo, tmp]);
    await execa('git', ['-C', tmp, 'push', 'origin', `${tag}:refs/heads/main`]);
}
