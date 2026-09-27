export type Category = 'water'|'electricity'|'sanitation'|'roads'|'streetlights'|'other';
export type Priority = 'high'|'normal'|'low'; export type Status = 'open'|'in_progress'|'resolved'|'rejected';
export type Provider = 'llm:groq'|'llm:ollama'|'rules'|'rules:fallback';
export interface Complaint {id:string;text:string;location:string;reporter_contact?:string;category:Category;priority:Priority;status:Status;ai_summary:string;triaged_by:Provider;created_at:string;updated_at:string}
export interface ComplaintInput {text:string;location:string;reporter_contact?:string} export interface ComplaintFilters {category?:Category;priority?:Priority;status?:Status;page?:number;page_size?:number}
export interface ComplaintListResponse {items:Complaint[];page:number;page_size:number;total:number} export interface Stats {total:number;by_category:Record<Category,number>;by_priority:Record<Priority,number>;resolved:number} export interface ApiError {detail:string;status?:number}
