export async function recommendPins(gh, username, redis) {
    const cacheKey = `pins:${username}`;
    const cached = await redis.get(cacheKey);
    if (cached)
        return JSON.parse(cached);
    const repos = await gh.reposByUser(username);
    const now = Date.now();
    const scored = repos.map(r => {
        const updated = new Date(r.pushedAt || r.updatedAt).getTime();
        const days = Math.max(1, (now - updated) / (1000 * 60 * 60 * 24));
        const recency = 100 / days;
        const stars = Math.log10(1 + r.stargazerCount) * 20;
        const forks = Math.log10(1 + r.forkCount) * 10;
        const relevance = /hypercode|broksi|adhd|welshdog/i.test(r.description || '') ? 15 : 0;
        const score = recency + stars + forks + relevance;
        return { ...r, score };
    });
    const top = scored.sort((a, b) => b.score - a.score).slice(0, 6);
    await redis.set(cacheKey, JSON.stringify(top), 'EX', 3600);
    return top;
}
