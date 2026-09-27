import type {ApiError} from './types';
export const apiBaseUrl=()=>window.__CONFIG__?.API_URL || '/api';
export class ApiRequestError extends Error implements ApiError { status?: number; detail:string; constructor(detail:string,status?:number){super(detail);this.detail=detail;this.status=status;this.name='ApiRequestError';} }
export async function apiFetchResponse<T>(path:string,init:RequestInit={}):Promise<{data:T;response:Response}>{const response=await fetch(`${apiBaseUrl()}${path}`,{...init,headers:{'Content-Type':'application/json',...(init.headers||{})}});const body=await response.json().catch(()=>({}));if(!response.ok)throw new ApiRequestError(body.detail||response.statusText,response.status);return {data:body as T,response};}
export async function apiFetch<T>(path:string,init?:RequestInit):Promise<T>{return (await apiFetchResponse<T>(path,init)).data;}
