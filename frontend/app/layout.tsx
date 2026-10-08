import './globals.css';
import type { Metadata } from 'next';
export const metadata: Metadata={title:'Route 53 — AWS Console Clone',description:'A realistic Route 53 management console clone'};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body>{children}</body></html>}
