import {useState} from 'react';
import type {Complaint,Status} from '../../api/types';
import {updateComplaintStatus} from '../../api/complaints';

export default function StatusDropdown({complaint,onUpdated}:{complaint:Complaint;onUpdated:(c:Complaint)=>void}){
  const [error,setError]=useState('');
  async function change(status:Status){
    setError('');
    try{onUpdated(await updateComplaintStatus(complaint.id,status));}
    catch(err){const x=err as {detail:string;status?:number};setError(x.detail||'Unable to update status');}
  }
  return <div><select className="status-select" value={complaint.status} onChange={e=>change(e.target.value as Status)}>{['open','in_progress','resolved','rejected'].map(x=><option key={x} value={x}>{x.replace('_',' ')}</option>)}</select>{error&&<div className="status-error"><b>⚠ Unable to update status</b><span>{error}</span></div>}</div>;
}
