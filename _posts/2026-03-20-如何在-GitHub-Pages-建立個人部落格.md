---
layout: post
title: "如何在 GitHub Pages 建立個人部落格"
date: 2026-03-20
categories: 技術
tags: [GitHub, Jekyll, 教學, 網頁開發]
comments_count: 5
image: /assets/images/featured/如何在-github-pages-建立個人部落格.svg
---

GitHub Pages 是一個非常方便的靜態網站託管服務，您可以免費將您的網站部署在 GitHub 上。在本文中，我們將詳細介紹如何從零開始建立一個個人部落格，並將其部署到 GitHub Pages 上。

## 什麼是 GitHub Pages？

GitHub Pages 是 GitHub 提供的免費靜態網站託管服務，允許用戶直接從 GitHub 儲存庫托管網站。它支援 Jekyll 這個靜態網站生成器，使得建立和維護部落格變得非常簡單。

## 設置步驟

### 1. 創建 GitHub 帳戶

如果您還沒有 GitHub 帳戶，首先需要在 GitHub 上註冊一個帳戶。

### 2. 創建儲存庫

登入後，創建一個新的儲存庫，命名為 `username.github.io`，其中 username 是您的 GitHub 用戶名。這個特殊的儲存庫名稱會告訴 GitHub 這是一個 GitHub Pages 專案。

### 3. 安裝 Jekyll

Jekyll 是一個靜態網站生成器，專為部落格設計。您需要在本地安裝 Jekyll 來開發和測試您的網站。

首先，確保您已安裝 Ruby：

```bash
ruby -v