import { Readability } from '@mozilla/readability';
import { JSDOM } from 'jsdom';

function runReadability(html: string): string | null {
  const dom = new JSDOM(html);
  const article = new Readability(dom.window.document).parse();
  return article?.textContent ?? null;
}

describe('Readability extraction', () => {
  it('extracts content from simple HTML', () => {
    const html = `<html><body><article><h1>Hi</h1><p>Test</p></article></body></html>`;
    const text = runReadability(html);
    expect(text?.trim()).toBe('Hi\nTest');
  });

  it('returns null on empty page', () => {
    const html = `<html><body></body></html>`;
    const text = runReadability(html);
    expect(text).toBeNull();
  });
});
