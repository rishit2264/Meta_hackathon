# ContractEnv Frontend — Next.js

## Quick Start

```bash
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local with your backend URL
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Build for HF Spaces (static export)

```bash
npm run build
# Output in /out directory — copy to FastAPI /static
```

## Project Structure

```
src/
  app/           → App Router (layout, page, CSS)
  components/    → Sidebar, NegotiatePanel, HistoryPanel, APIPanel, ScoresPanel, RewardSidebar, GradeModal
    ui/          → Badge, Button, ScoreBar, JsonViewer
  hooks/         → useEpisode, useHealthCheck
  lib/           → Axios API client
  types/         → TypeScript types mirroring backend models
```
