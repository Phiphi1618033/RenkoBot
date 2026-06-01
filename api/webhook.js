import fetch from 'node-fetch';

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;
  const { ticker, signal, entry, stopLoss, takeProfit, wins, losses, winRate } = body;

  const chatId = req.query.chat_id || process.env.CHAT_ID;
  if (!chatId) return res.status(400).json({ error: 'Missing chat_id' });

  const emoji = signal === 'BUY' ? '🟢' : '🔴';
  const text = [
    `${emoji} *${signal} Signal* ${ticker}`,
    `Entry: \`${entry}\``,
    `Stop Loss: \`${stopLoss}\``,
    `Take Profit: \`${takeProfit}\``,
    `Wins: ${wins}  •  Losses: ${losses}`,
    `Win Rate: ${winRate}%`
  ].join('\n');

  try {
    const resp = await fetch(`https://api.telegram.org/bot${process.env.BOT_TOKEN}/sendMessage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: chatId,
        text,
        parse_mode: 'MarkdownV2',
        disable_web_page_preview: true
      })
    });
    const data = await resp.json();
    if (!data.ok) throw new Error(data.description);
    res.status(200).json({ success: true });
  } catch (e) {
    console.error(e);
    res.status(500).json({ error: 'Telegram send failed' });
  }
}
