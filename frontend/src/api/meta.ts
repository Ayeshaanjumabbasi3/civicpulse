import {apiFetch} from './client';
import type {ApiContract} from './types';
export function getApiContract(): Promise<ApiContract> { return apiFetch<ApiContract>('/meta/contract'); }
