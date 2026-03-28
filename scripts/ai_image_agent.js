#!/usr/bin/env node
/**
 * AI Image Agent - 使用 Agent Browser + Pollinations AI 生成真實 AI 圖片
 * 
 * 使用方式:
 *   node ai_image_agent.js "文章標題" "分類" [輸出目錄]
 * 
 * 示例:
 *   node ai_image_agent.js "提升工作效率的五個實用技巧" "生活" "./assets/images/featured/"
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// 分類對應的風格提示詞
const STYLE_PROMPTS = {
  '技術': 'technology, modern, professional, blue tones, sleek design, digital, minimalist, tech illustration',
  '生活': 'lifestyle, warm, cozy, natural lighting, everyday life, friendly atmosphere, warm colors',
  '健康': 'health, wellness, nature, green tones, fresh, vibrant, organic, wellness illustration',
  '投資': 'finance, business, professional, gold and dark blue, wealth, growth, charts, business illustration',
  'default': 'beautiful, clean, modern illustration, professional, minimalist art'
};

// 預設圖片尺寸
const IMAGE_WIDTH = 1024;
const IMAGE_HEIGHT = 576;

/**
 * 執行 agent-browser 命令
 */
function ab(args) {
  const cmd = ['agent-browser', ...args].join(' ');
  console.log(`> ${cmd}`);
  try {
    return execSync(cmd, { 
      encoding: 'utf8',
      timeout: 180000,
      stdio: ['pipe', 'pipe', 'pipe']
    });
  } catch (error) {
    return null;
  }
}

/**
 * 根據文章標題和分類生成 AI 圖片
 */
async function generateImage(title, category, outputDir = './assets/images/featured/') {
  const style = STYLE_PROMPTS[category] || STYLE_PROMPTS['default'];
  const prompt = `${title}, ${style}, high quality illustration, no text`;
  
  // 清理標題作為檔名
  const safeTitle = title.replace(/[^a-zA-Z0-9\u4e00-\u9fff]/g, '-').substring(0, 50);
  const filename = safeTitle + '.png';
  const outputPath = path.join(outputDir, filename);
  
  console.log(`\n🎨 AI 圖片生成器`);
  console.log(`═══════════════════════════════════════`);
  console.log(`   標題: ${title}`);
  console.log(`   分類: ${category}`);
  console.log(`   Prompt: ${prompt}`);
  console.log(`   輸出: ${outputPath}`);
  console.log(`═══════════════════════════════════════\n`);
  
  // 確保輸出目錄存在
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  try {
    // 方法 1: 直接使用 Pollinations URL 格式
    const encodedPrompt = encodeURIComponent(prompt);
    const pollinationsUrl = `https://pollinations.ai/prompt/${encodedPrompt}?width=${IMAGE_WIDTH}&height=${IMAGE_HEIGHT}&nologo=true&seed=${Math.floor(Math.random() * 1000000)}`;
    
    console.log(`📡 打開 Pollinations AI...`);
    ab(['open', pollinationsUrl]);
    
    // 等待頁面加載和圖片生成
    console.log(`⏳ 等待圖片生成 (10 秒)...`);
    ab(['wait', '10000']);
    
    // 截圖
    const screenshotPath = '/tmp/ai_generated_image.png';
    console.log(`📸 截圖中...`);
    ab(['screenshot', screenshotPath]);
    
    // 檢查截圖是否存在
    if (fs.existsSync(screenshotPath)) {
      // 複製到目標位置
      fs.copyFileSync(screenshotPath, outputPath);
      
      const stats = fs.statSync(outputPath);
      console.log(`\n✅ 圖片生成成功!`);
      console.log(`   檔案: ${outputPath}`);
      console.log(`   大小: ${(stats.size / 1024).toFixed(1)} KB`);
      console.log(`   尺寸: ${IMAGE_WIDTH}x${IMAGE_HEIGHT}px`);
      
      // 清理臨時檔案
      fs.unlinkSync(screenshotPath);
      
      return outputPath;
    } else {
      throw new Error('截圖失敗');
    }
    
  } catch (error) {
    console.error(`\n❌ 生成失敗: ${error.message}`);
    throw error;
  } finally {
    // 關閉瀏覽器
    ab(['close']);
    console.log(`🔚 瀏覽器已關閉`);
  }
}

/**
 * 批量生成多篇文章的圖片
 */
async function batchGenerate(articles, outputDir) {
  console.log(`\n📚 批量生成 ${articles.length} 篇文章的圖片...\n`);
  
  const results = [];
  for (const article of articles) {
    try {
      const result = await generateImage(article.title, article.category, outputDir);
      results.push({ title: article.title, status: 'success', path: result });
    } catch (error) {
      results.push({ title: article.title, status: 'failed', error: error.message });
    }
  }
  
  console.log(`\n📊 批量生成結果:`);
  results.forEach(r => {
    console.log(`   ${r.status === 'success' ? '✅' : '❌'} ${r.title}`);
  });
  
  return results;
}

// 主程式
async function main() {
  const args = process.argv.slice(2);
  
  // 測試模式
  if (args[0] === '--test') {
    console.log('🧪 測試模式\n');
    await generateImage('測試圖片', '技術', '/tmp/');
    return;
  }
  
  if (args.length < 1) {
    console.log(`
╔═══════════════════════════════════════════════════════════╗
║              AI Image Agent - 使用說明                     ║
╠═══════════════════════════════════════════════════════════╣
║  使用方式:                                                 ║
║    node ai_image_agent.js "文章標題" "分類" [輸出目錄]     ║
║                                                             ║
║  參數說明:                                                 ║
║    文章標題  - 文章的標題 (必填)                            ║
║    分類      - 文章分類: 技術/生活/健康/投資 (預設: default)║
║    輸出目錄  - 圖片儲存位置 (預設: ./assets/images/featured/)║
║                                                             ║
║  範例:                                                     ║
║    node ai_image_agent.js "提升工作效率的五個實用技巧" "生活"    ║
║    node ai_image_agent.js --test                           ║
╚═══════════════════════════════════════════════════════════╝
`);
    process.exit(1);
  }
  
  const title = args[0];
  const category = args[1] || 'default';
  const outputDir = args[2] || './assets/images/featured/';
  
  try {
    await generateImage(title, category, outputDir);
  } catch (error) {
    console.error('錯誤:', error.message);
    process.exit(1);
  }
}

module.exports = { generateImage, batchGenerate };

if (require.main === module) {
  main();
}