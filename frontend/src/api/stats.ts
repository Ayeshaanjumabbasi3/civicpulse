import type {Stats} from './types'; import {apiFetchResponse} from './client';
export async function getStats():Promise<Stats & {_cache:'HIT'|'MISS'}>{const {data,response}=await apiFetchResponse<Stats>('/stats');const cache=response.headers.get('X-Cache');return {...data,_cache:cache==='HIT'?'HIT':'MISS'};}
