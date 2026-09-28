import {useEffect,useState} from 'react';
import {getApiContract} from '../api/meta';
import type {ApiContract} from '../api/types';
export function useApiContract(){const [data,setData]=useState<ApiContract|null>(null);const [error,setError]=useState('');useEffect(()=>{getApiContract().then(setData).catch(e=>setError(e instanceof Error?e.message:'Unable to load API contract'))},[]);return {data,error};}
