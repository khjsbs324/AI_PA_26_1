from pathlib import Path
import re

index_path = Path('index.html')
style_path = Path('style.css')
index = index_path.read_text(encoding='utf-8')
style = style_path.read_text(encoding='utf-8')

checklist_text = '''■ 프롬프트 체크리스트

1. 첫 실행 조사 기간이 최근 7일인가?
2. 웹 검색을 실제로 사용했는가?
3. 핵심 업데이트가 3개 이하인가?
4. 중요하지 않은 일반 AI 뉴스가 제외됐는가?
5. 각 항목에 발표일 또는 변경일이 있는가?
6. 발표일과 기사 게시일을 구분했는가?
7. 핵심 정보에 공식 출처가 있는가?
8. 가격·플랜·크레딧을 공식 페이지에서 확인했는가?
9. 순차 배포·베타·국가·요금제 제한을 표시했는가?
10. 강의 자료 반영 필요 여부가 명확한가?
11. 학생 실습 아이디어가 실제 수업에 적용 가능한가?
12. 동일 발표를 여러 항목으로 중복 작성하지 않았는가?
13. 오래된 기사나 재게시 기사가 포함되지 않았는가?
14. 확인 전 정보를 사실처럼 작성하지 않았는가?
15. 직접 연결되는 출처 링크가 정상적으로 열리는가?
16. 주요 정보가 없을 때 지정된 한 문장만 출력하는가?

※ 다음 중 하나라도 발생하면 첫 실행은 실패로 판단합니다.

1. 존재하지 않는 링크
2. 잘못된 가격·날짜·지원 국가
3. 공식 확인이 없는 내용을 공식 확인으로 표시
4. 이전 발표를 신규 발표로 오인
5. 중요 정보를 만들거나 추정하여 작성'''

if 'const promptChecklistText =' not in index:
    anchor = '      try{\n'
    insertion = '      const promptChecklistText = ' + repr(checklist_text) + ';\n\n'
    index = index.replace(anchor, insertion + anchor, 1)

if '.prompt-checklist-section{' not in index:
    style_anchor = '          .personality-section{background:linear-gradient(180deg,#ffffff 0%,#f7f9ff 100%)}\n'
    style_add = '''          .prompt-checklist-section{background:linear-gradient(180deg,#ffffff 0%,#f7f9ff 100%)}
          .prompt-checklist-block{padding:24px;border:1px solid var(--line);border-radius:22px;background:#fff;box-shadow:0 12px 28px rgba(23,24,33,.05)}
          .prompt-checklist-block h3{margin:0 0 14px;color:var(--ink);font-size:22px;line-height:1.4;letter-spacing:-.03em}
          .prompt-checklist-block pre{margin:0;white-space:pre-wrap;word-break:keep-all;background:#111827;color:#eef2ff;border-radius:18px;padding:22px;line-height:1.8;overflow:auto}
          .prompt-checklist-block code{display:block;padding-right:38px;font-size:15px}
'''
    index = index.replace(style_anchor, style_anchor + style_add, 1)

if "promptChecklistSection.id = 'prompt-checklist'" not in index:
    anchor = "        const personalitySection = originalDoc.createElement('section');\n"
    section = '''        const promptChecklistSection = originalDoc.createElement('section');
        promptChecklistSection.id = 'prompt-checklist';
        promptChecklistSection.className = 'section prompt-checklist-section';
        promptChecklistSection.setAttribute('aria-labelledby', 'prompt-checklist-title');
        promptChecklistSection.innerHTML = `
          <div class="section-title">
            <p class="number">추가 자료</p>
            <h2 id="prompt-checklist-title">프롬프트 체크리스트</h2>
            <p>첫 실행 결과의 조사 기간, 출처, 최신성, 정확성과 중복 여부를 순서대로 검수합니다.</p>
          </div>
          <article class="prompt-checklist-block">
            <h3>프롬프트 체크리스트 전체</h3>
            <pre><code></code></pre>
          </article>
        `;
        promptChecklistSection.querySelector('code').textContent = promptChecklistText;

'''
    index = index.replace(anchor, section + anchor, 1)

index = index.replace(
    "          wrapup.parentNode.insertBefore(section, wrapup);\n          wrapup.parentNode.insertBefore(personalitySection, wrapup);",
    "          wrapup.parentNode.insertBefore(section, wrapup);\n          wrapup.parentNode.insertBefore(promptChecklistSection, wrapup);\n          wrapup.parentNode.insertBefore(personalitySection, wrapup);",
    1,
)
index = index.replace(
    "          originalDoc.querySelector('main').appendChild(section);\n          originalDoc.querySelector('main').appendChild(personalitySection);",
    "          originalDoc.querySelector('main').appendChild(section);\n          originalDoc.querySelector('main').appendChild(promptChecklistSection);\n          originalDoc.querySelector('main').appendChild(personalitySection);",
    1,
)

style = re.sub(r'\n?/\* 강사 기준 프롬프트:.*?@media\(max-width:640px\)\{#brand-prompts::after\{.*?\}\}\s*$', '\n', style, flags=re.S)
style += '\n#brand-prompts::after{content:none!important;display:none!important}\n'

index_path.write_text(index, encoding='utf-8')
style_path.write_text(style, encoding='utf-8')
