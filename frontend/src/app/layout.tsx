import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: 'ContractEnv — AI Contract Negotiation',
  description: 'Two AI agents negotiate your business contract. Private constraints, live streaming, autonomous agreement.',
  openGraph: { 
    title: 'ContractEnv — AI Contract Negotiation', 
    description: 'Two AI agents negotiate your business contract.', 
    type: 'website' 
  }
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <div className="min-h-screen bg-pink-50 text-charcoal font-sans">
          {children}
        </div>
      </body>
    </html>
  );
}
