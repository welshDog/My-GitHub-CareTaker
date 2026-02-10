function norm(s) { return (s || '').toLowerCase().replace(/[^a-z0-9]/g, ''); }
function sim(a, b) {
    const na = norm(a), nb = norm(b);
    let match = 0;
    const len = Math.max(na.length, nb.length);
    if (len === 0)
        return 0;
    for (let i = 0; i < Math.min(na.length, nb.length); i++) {
        if (na[i] === nb[i])
            match++;
    }
    return match / len;
}
export async function findDuplicates(gh, username, redis) {
    const cacheKey = `dups:${username}`;
    const cached = await redis.get(cacheKey);
    if (cached)
        return JSON.parse(cached);
    const repos = await gh.reposByUser(username);
    const pairs = [];
    for (let i = 0; i < repos.length; i++) {
        for (let j = i + 1; j < repos.length; j++) {
            const a = repos[i], b = repos[j];
            const nameSim = sim(a.name, b.name);
            const descSim = sim(a.description || '', b.description || '');
            const pushedDiff = Math.abs(new Date(a.pushedAt).getTime() - new Date(b.pushedAt).getTime()) / (1000 * 60 * 60 * 24);
            const commitPattern = pushedDiff < 14 ? 0.2 : 0;
            const score = (nameSim * 0.6) + (descSim * 0.2) + commitPattern;
            if (score > 0.7) {
                pairs.push({ a: a.name, b: b.name, score });
            }
        }
    }
    await redis.set(cacheKey, JSON.stringify(pairs), 'EX', 1800);
    return pairs;
}
