import "./globals.css";

export const metadata = {
  title: "Ecom CRM Admin",
  description: "Internal admin UI"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="container">
          <header className="header">
            <div>
              <div className="title">Ecom CRM Admin</div>
              <div className="subtitle">Internal dashboard</div>
            </div>
          </header>
          {children}
          <footer className="footer">
            API UI lives at <code>/docs</code> on the backend
          </footer>
        </div>
      </body>
    </html>
  );
}
