import fetch from 'node-fetch';
export async function enhanceReadme(gh, owner, repo, headerMd, svg, redis) {
    const repoQ = `https://api.github.com/repos/${owner}/${repo}`;
    const rr = await fetch(repoQ, { headers: { Authorization: `Bearer ${process.env.GH_TOKEN}` } });
    const repoJson = await rr.json();
    const defaultBranch = repoJson.default_branch || 'main';
    const readmeUrl = `https://api.github.com/repos/${owner}/${repo}/contents/README.md?ref=${defaultBranch}`;
    const r = await fetch(readmeUrl, { headers: { Authorization: `Bearer ${process.env.GH_TOKEN}` } });
    const readme = await r.json();
    const beforeContent = Buffer.from(readme.content || '', 'base64').toString('utf-8');
    const afterContent = `${headerMd}\n\n${beforeContent}`;
    const branch = `caretaker/readme-${Date.now()}`;
    await fetch(`https://api.github.com/repos/${owner}/${repo}/git/refs`, {
        method: 'POST', headers: { Authorization: `Bearer ${process.env.GH_TOKEN}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ ref: `refs/heads/${branch}`, sha: repoJson.default_branch_sha || repoJson.sha || repoJson.head || repoJson.pushed_at })
    }).catch(() => { });
    await fetch(`https://api.github.com/repos/${owner}/${repo}/contents/.caretaker/banner.svg`, {
        method: 'PUT', headers: { Authorization: `Bearer ${process.env.GH_TOKEN}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: 'Add README banner', content: Buffer.from(svg).toString('base64'), branch })
    });
    await fetch(`https://api.github.com/repos/${owner}/${repo}/contents/README.md`, {
        method: 'PUT', headers: { Authorization: `Bearer ${process.env.GH_TOKEN}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: 'Enhance README header', content: Buffer.from(afterContent).toString('base64'), branch, sha: readme.sha })
    });
    await redis.hset(`readme:snapshot:${owner}:${repo}`, 'content', beforeContent);
    const prResp = await fetch(`https://api.github.com/repos/${owner}/${repo}/pulls`, {
        method: 'POST', headers: { Authorization: `Bearer ${process.env.GH_TOKEN}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: 'CareTaker README Enhancement', head: branch, base: defaultBranch, body: `Automated README enhancement. Includes banner and badges.` })
    });
    const pr = await prResp.json();
    await fetch(`https://api.github.com/repos/${owner}/${repo}/pulls/${pr.number}/requested_reviewers`, {
        method: 'POST', headers: { Authorization: `Bearer ${process.env.GH_TOKEN}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ reviewers: [] })
    });
    await fetch(`https://api.github.com/repos/${owner}/${repo}/branches/${defaultBranch}/protection`, {
        method: 'PUT', headers: { Authorization: `Bearer ${process.env.GH_TOKEN}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ required_pull_request_reviews: { required_approving_review_count: 2 } })
    });
    return pr;
}
export async function rollbackReadme(owner, repo, redis) {
    const content = await redis.hget(`readme:snapshot:${owner}:${repo}`, 'content');
    if (!content)
        return { ok: false };
    const branch = `caretaker/rollback-${Date.now()}`;
    await fetch(`https://api.github.com/repos/${owner}/${repo}/contents/README.md`, {
        method: 'PUT', headers: { Authorization: `Bearer ${process.env.GH_TOKEN}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: 'Rollback README', content: Buffer.from(content).toString('base64'), branch })
    });
    const prResp = await fetch(`https://api.github.com/repos/${owner}/${repo}/pulls`, {
        method: 'POST', headers: { Authorization: `Bearer ${process.env.GH_TOKEN}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: 'CareTaker README Rollback', head: branch, base: 'main', body: 'Rollback after failing tests.' })
    });
    const pr = await prResp.json();
    return pr;
}
