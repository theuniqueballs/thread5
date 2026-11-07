import type { Metadata } from "next";
import { Manrope, JetBrains_Mono, Unbounded } from "next/font/google";
import "./globals.css";
import { Toaster } from "@/components/ui/toaster";

/* Дисплей — заголовки, цифры, лого. Manrope — текст. JB Mono — терминал/промпты. Все три — с кириллицей. */
const fontDisplay = Unbounded({
  subsets: ["latin", "cyrillic"],
  variable: "--font-unbounded",
});

const fontSans = Manrope({
  subsets: ["latin", "cyrillic"],
  variable: "--font-manrope",
});

const fontMono = JetBrains_Mono({
  subsets: ["latin", "cyrillic"],
  variable: "--font-jbmono",
});

export const metadata: Metadata = {
  title: "THREAD 5 — прилавок",
  description:
    "Прилавок Thread 5: батчи RAW+ для Tsubaki.2 Pro → Yodayo. Чат — двигатель, файлы — память, прилавок — посмотреть, скопировать POS/NEG, дать вердикт.",
  icons: {
    icon: "https://z-cdn.chatglm.cn/z-ai/static/logo.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ru" suppressHydrationWarning>
      <body
        className={`${fontDisplay.variable} ${fontSans.variable} ${fontMono.variable} font-sans antialiased bg-background text-foreground`}
      >
        {children}
        <Toaster />
      </body>
    </html>
  );
}
