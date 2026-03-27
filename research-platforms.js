// 研究無 CAPTCHA 的 GPT 平台
const platforms = [
  { name: 'Picoworkers', url: 'https://picoworkers.com', notes: '微任務平台' },
  { name: 'SproutGigs', url: 'https://sproutgigs.com', notes: '前 Picoworkers' },
  { name: 'RapidWorkers', url: 'https://rapidworkers.com', notes: '微任務' },
  { name: 'Clickworker', url: 'https://clickworker.com', notes: '需評估測試' },
  { name: 'HiveMicro', url: 'https://hivemicro.com', notes: 'AI 訓練任務' }
];

console.log('📋 備選平台清單：');
platforms.forEach((p, i) => {
  console.log(`${i+1}. ${p.name} - ${p.url}`);
  console.log(`   ${p.notes}`);
});
