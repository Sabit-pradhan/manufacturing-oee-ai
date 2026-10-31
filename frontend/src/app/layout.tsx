
import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "YottaFlex | Manufacturing Intelligence",
  description:
    "Industrial manufacturing monitoring, OEE analytics and AI anomaly detection dashboard.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
