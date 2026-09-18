import './globals.css';
import Sidebar from '@/components/Sidebar';

export const metadata = {
  title: 'StackOfFifty — Cybersecurity Defense & Operations Platform',
  description: 'Enterprise modular Blue Team cybersecurity telemetry, detection, and compliance framework',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-zinc-950 text-slate-100 flex min-h-screen">
        <Sidebar />
        <main className="flex-1 overflow-y-auto max-h-screen bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(6,182,212,0.1),rgba(255,255,255,0))]">
          {children}
        </main>
      </body>
    </html>
  );
}
