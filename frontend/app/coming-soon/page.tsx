'use client';
import {useEffect,useState} from 'react';
import ConsoleShell from '../../components/ConsoleShell';
export default function ComingSoon(){
  const [section,setSection]=useState('This section');
  useEffect(()=>{setSection(new URLSearchParams(window.location.search).get('section')||'This section')},[]);
  return <ConsoleShell><div className="crumb">Route 53 <span>/</span> {section}</div><div className="empty-page"><h1>{section}</h1><p>This section is mocked for the assignment and is not part of the implemented Route 53 workflow.</p><button className="primary" onClick={()=>window.location.href='/'}>Back to Hosted zones</button></div></ConsoleShell>
}
