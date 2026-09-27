export default function CacheStatus({state}:{state:'HIT'|'MISS'}){return <div className="cache-status"><i/> Cache {state} <span>— Updated just now</span></div>}
