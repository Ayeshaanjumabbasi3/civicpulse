import {useState} from 'react';
import type {Complaint,Status,ApiContract} from '../../api/types';
import {updateComplaintStatus} from '../../api/complaints';
export default function StatusDropdown({complaint,onUpdated,contract}:{complaint:Complaint;onUpdated:(c:Complaint)=>void;contract:ApiContract}){const [error,setError]=useState('');async function change(status:Status){setError('');try{onUpdated(await updateComplaintStatus(complaint.id,status))}catch(err){const x=err as {detail:string};setError(x.detail||'Unable to update status')}}const options=[complaint.status,...contract.transitions[complaint.status]].filter((x,i,a)=>a.indexOf(x)===i);return <div><select className="status-select" value={complaint.status} onChange={e=>change(e.target.value as Status)}>{options.map(x=><option key={x} value={x}>{x.replace('_',' ')}</option>)}</select>{error&&<div className="status-error"><b>⚠ Unable to update status</b><span>{error}</span></div>}</div>}

