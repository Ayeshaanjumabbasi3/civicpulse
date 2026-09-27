import type {Complaint,ComplaintFilters,ComplaintInput,ComplaintListResponse,Status} from './types'; import {apiFetch} from './client';
const query=(filters:ComplaintFilters)=>{const params=new URLSearchParams();Object.entries(filters).forEach(([key,value])=>{if(value!==undefined)params.set(key,String(value));});const value=params.toString();return value?`?${value}`:'';};
export function createComplaint(input:ComplaintInput):Promise<Complaint>{return apiFetch<Complaint>('/complaints',{method:'POST',body:JSON.stringify(input)});}
export function getComplaint(id:string):Promise<Complaint|undefined>{return apiFetch<Complaint>(`/complaints/${encodeURIComponent(id)}`);}
export function getComplaints(filters:ComplaintFilters={}):Promise<ComplaintListResponse>{return apiFetch<ComplaintListResponse>(`/complaints${query(filters)}`);}
export function updateComplaintStatus(id:string,status:Status):Promise<Complaint>{return apiFetch<Complaint>(`/complaints/${encodeURIComponent(id)}/status`,{method:'PATCH',body:JSON.stringify({status})});}
