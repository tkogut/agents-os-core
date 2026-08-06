import { describe, it, expect, beforeEach, vi } from 'vitest';
import fs from 'fs';
import path from 'path';

// Szablon testu jednostkowego frontendu SPA z symulacją DOM w Vitest
const indexHtmlContent = fs.readFileSync(path.resolve(__dirname, '../../src/static/index.html'), 'utf8');

describe('Frontend Component Tests', () => {
  let appModule;

  beforeEach(() => {
    // Załadowanie struktury DOM z rzeczywistego pliku HTML
    document.body.innerHTML = indexHtmlContent;
    
    // Mockowanie globalnych zależności
    global.window.showToast = vi.fn();
    global.window.fetch = vi.fn().mockImplementation(() => 
      Promise.resolve({
        ok: true,
        status: 200,
        json: () => Promise.resolve({ status: "success" })
      })
    );
    
    // Inicjalizacja skryptu app.js w kontekście JSDOM
    if (!appModule) {
      const appJsCode = fs.readFileSync(path.resolve(__dirname, '../../src/static/app.js'), 'utf8');
      const runCode = new Function('window', 'document', 'console', appJsCode);
      runCode(window, document, console);
      
      // Wyzwalacz zdarzenia ładowania DOM
      window.document.dispatchEvent(new window.Event('DOMContentLoaded'));
      
      appModule = {
        prettyModelName: window.prettyModelName,
        renderAnalyticsChart: window.renderAnalyticsChart
      };
    }
  });

  it('powinien formatować nazwy modeli', () => {
    expect(appModule.prettyModelName('gemini-2.5-flash')).toBe('Gemini 2.5 Flash');
  });
});
