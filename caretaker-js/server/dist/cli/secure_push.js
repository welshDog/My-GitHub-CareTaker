import readline from 'readline';
import { securePushFlow, rollback } from '../push_guard';
const repo = process.argv[2] || 'https://github.com/welshDog/GitHub-Hyper-Agent-BROski.git';
const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
rl.question(`Proceed with secure push to ${repo}? Type YES to continue: `, async (ans) => {
    if (ans !== 'YES') {
        console.log('Aborted');
        rl.close();
        return;
    }
    try {
        const r = await securePushFlow(repo);
        console.log('OK', r.logPath);
    }
    catch (e) {
        console.error('Failed', e);
        await rollback(repo, 'backup/main');
    }
    rl.close();
});
