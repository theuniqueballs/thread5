import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  /* 2026-11-16: TS-ошибки вычищены (inbox/route/lightbox/extractJson), ignoreBuildErrors
     снят — сборка снова ловит типы. Скрафтовые examples/mini-services/tests выведены
     из tsconfig.exclude, чтобы чужой код не ломал проверку. */
  reactStrictMode: false,
};

export default nextConfig;
