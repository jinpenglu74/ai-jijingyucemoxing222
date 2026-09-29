from pathlib import Path
import sys, shutil
root = Path(sys.argv[1]).resolve()
overlay = Path(__file__).resolve().parent
src = root / 'src'

# Copy new experience module
shutil.copy2(overlay / 'experience.h', src / 'experience.h')
shutil.copy2(overlay / 'experience.c', src / 'experience.c')

# storage path
p = src / 'storage.h'
s = p.read_text(encoding='utf-8')
needle = '    WCHAR review_path[DATA_ROOT_CAP];\n'
if 'experience_path' not in s:
    s = s.replace(needle, needle + '    WCHAR experience_path[DATA_ROOT_CAP];\n')
p.write_text(s, encoding='utf-8')

p = src / 'storage.c'
s = p.read_text(encoding='utf-8')
needle = '    build_path(ctx->review_path,DATA_ROOT_CAP,ctx->root,L"\\\\data\\\\reviews_v1.bin");\n'
if 'experience_store_v1.bin' not in s:
    s = s.replace(needle, needle + '    build_path(ctx->experience_path,DATA_ROOT_CAP,ctx->root,L"\\\\data\\\\experience_store_v1.bin");\n')
p.write_text(s, encoding='utf-8')

# DeepSeek: experience-aware prompt + retrieval
p = src / 'deepseek.c'
s = p.read_text(encoding='utf-8')
if '#include "experience.h"' not in s:
    s = s.replace('#include "prediction_repair.h"\n', '#include "prediction_repair.h"\n#include "experience.h"\n')
s = s.replace('#define PREDICTION_PROMPT_VERSION 1', '#define PREDICTION_PROMPT_VERSION 2')
old_start = 'static void build_body(Buf* b,const FundRecord* f,const MarketSnapshot* m,int model_kind)'
if old_start in s:
    a = s.index(old_start)
    b = s.index('\n\nstatic void build_headers', a)
    new = '''static void build_body(const StorageContext* st,Buf* b,const FundRecord* f,const MarketSnapshot* m,int model_kind){static const char* system_prompt="You are the forecasting engine of an AI fund research application. Use only the supplied snapshot evidence. Never invent missing facts. Forecast six horizons independently: TODAY, NEXT_DAY, THIS_WEEK, NEXT_WEEK, THIS_MONTH, NEXT_MONTH. Historical experience is advisory evidence only: never treat it as a fact about the current market, never override contradictory current snapshot evidence, and reduce confidence when current evidence is weak. This is probabilistic research, not investment advice. Return one valid JSON object only. All explanation text must be concise Simplified Chinese. For each horizon return direction UP/FLAT/DOWN, integer p_up/p_flat/p_down summing exactly 100, return_low_x100 and return_high_x100 where 100 means 1.00%, confidence 0-100, summary, positive array max 3, negative array max 3, uncertainty array max 2, drivers array max 3. Confidence must reflect data quality. Do not output chain-of-thought or reasoning_content in the final JSON.";\n    bs(b,"{\\\"model\\\":");json_ascii(b,model_name_a(model_kind));bs(b,",\\\"messages\\\":[{\\\"role\\\":\\\"system\\\",\\\"content\\\":");json_ascii(b,system_prompt);bs(b,"},{\\\"role\\\":\\\"user\\\",\\\"content\\\":");\n    {Buf ev;char expctx[12288];int used=0;binit(&ev,49152);append_evidence(&ev,f,m);if(st&&experience_build_context_utf8(st,f,expctx,(int)sizeof(expctx),&used)&&used>0){WCHAR lm[160],n[24];bs(&ev,"\\nEXPERIENCE_CONTEXT=");bs(&ev,expctx);wcopy_d(lm,160,L"selected=");int_w(used,n,24);wcat_d(lm,160,n);storage_log_ex(st,L"INFO",L"EXPERIENCE_INJECT",f?f->code:NULL,lm);}else if(st){storage_log_ex(st,L"INFO",L"EXPERIENCE_INJECT",f?f->code:NULL,L"selected=0");}if(!ev.ok){b->ok=0;bfree(&ev);return;}bs(&ev,"\\nOUTPUT_SCHEMA={\\\"TODAY\\\":{...},\\\"NEXT_DAY\\\":{...},\\\"THIS_WEEK\\\":{...},\\\"NEXT_WEEK\\\":{...},\\\"THIS_MONTH\\\":{...},\\\"NEXT_MONTH\\\":{...}}");json_ascii(b,ev.p);bfree(&ev);}bs(b,"}],\\\"response_format\\\":{\\\"type\\\":\\\"json_object\\\"},\\\"reasoning_effort\\\":\\\"high\\\",\\\"max_tokens\\\":6000}");}\n'''
    s = s[:a] + new + s[b:]
s = s.replace('binit(&body,BODY_CAP);build_body(&body,f,m,model_kind);', 'binit(&body,BODY_CAP);build_body(st,&body,f,m,model_kind);')
p.write_text(s, encoding='utf-8')

# Main UI and sync chain
p = src / 'main.c'
s = p.read_text(encoding='utf-8')
if '#include "experience.h"' not in s:
    s = s.replace('#include "review.h"\n', '#include "review.h"\n#include "experience.h"\n')
s = s.replace('#define APP_TITLE L"AI基金预测 V0.6"', '#define APP_TITLE L"AI基金预测 V0.7"')
s = s.replace('V0.6 AI复盘基础版', 'V0.7 AI经验闭环基础版')
s = s.replace('开始构建V0.6预测输入', '开始构建V0.7预测输入')
func = r'''static void draw_experience_page(HDC dc,const LayoutInfo* L,HFONT small,HFONT body,HFONT bold,HFONT big){
    int dpi=L->dpi,x=L->content_x,y=L->header_h+s(20,dpi),w=L->content_w,i,n,rowY,rowH=s(74,dpi),cw,gap=s(10,dpi);ExperienceStats st;ExperienceRecord* rows;WCHAR num[32],buf[320];
    experience_get_stats(&gStorage,&st);cw=(w-gap*3)/4;
    {const WCHAR* labs[4]={L"经验总数",L"有效经验",L"观察经验",L"失败经验"};int vals[4]={st.total_count,st.active_count,st.observe_count,st.failure_count};COLORREF cs[4]={RGB(37,99,235),RGB(16,185,129),RGB(245,158,11),RGB(220,38,38)};for(i=0;i<4;i++){int l=x+i*(cw+gap);round_box(dc,l,y,l+cw,y+s(78,dpi),s(8,dpi),RGB(255,255,255),RGB(228,233,241));text(dc,labs[i],l+s(14,dpi),y+s(7,dpi),l+cw-s(10,dpi),y+s(34,dpi),RGB(95,108,128),small,DT_LEFT|DT_VCENTER|DT_SINGLELINE);int_text(vals[i],num,32);text(dc,num,l+s(14,dpi),y+s(32,dpi),l+cw-s(10,dpi),y+s(69,dpi),cs[i],big,DT_LEFT|DT_VCENTER|DT_SINGLELINE);}}
    y+=s(90,dpi);round_box(dc,x,y,x+w,L->height-L->footer_h-s(12,dpi),s(9,dpi),RGB(255,255,255),RGB(228,233,241));text(dc,L"AI经验库｜只保存通过真实结果+AI复盘质量门控的经验",x+s(16,dpi),y+s(6,dpi),x+w-s(16,dpi),y+s(38,dpi),RGB(31,41,55),bold,DT_LEFT|DT_VCENTER|DT_SINGLELINE);text(dc,L"经验不会直接覆盖当前事实；预测前最多召回5条同基金/同类型高质量经验，仅作为历史参考证据。幸运命中、UNSUPPORTED、低证据复盘不会进入有效经验库。",x+s(16,dpi),y+s(34,dpi),x+w-s(16,dpi),y+s(72,dpi),RGB(102,115,135),small,DT_LEFT|DT_WORDBREAK|DT_END_ELLIPSIS);
    rows=(ExperienceRecord*)HeapAlloc(GetProcessHeap(),HEAP_ZERO_MEMORY,sizeof(ExperienceRecord)*EXPERIENCE_LOAD_MAX);if(!rows)return;n=experience_load_latest(&gStorage,rows,EXPERIENCE_LOAD_MAX);rowY=y+s(82,dpi);
    for(i=0;i<n&&i<8;i++){ExperienceRecord* r=&rows[n-1-i];int yy=rowY+i*rowH;WCHAR score[32];if(yy+rowH>L->height-L->footer_h-s(18,dpi))break;line(dc,x+s(14,dpi),yy,x+w-s(14,dpi),yy,RGB(238,241,246),1);text(dc,(WCHAR*)r->fund_name,x+s(18,dpi),yy,x+s(210,dpi),yy+rowH,RGB(31,41,55),bold,DT_LEFT|DT_VCENTER|DT_SINGLELINE|DT_END_ELLIPSIS);text(dc,experience_type_name(r->experience_type),x+s(215,dpi),yy,x+s(315,dpi),yy+rowH,r->experience_type==EXPERIENCE_TYPE_FAILURE?RGB(220,38,38):RGB(16,130,100),small,DT_CENTER|DT_VCENTER|DT_SINGLELINE);int_text(r->score,score,32);text(dc,score,x+s(320,dpi),yy,x+s(370,dpi),yy+rowH,RGB(37,99,235),bold,DT_CENTER|DT_VCENTER|DT_SINGLELINE);text(dc,experience_status_name(r->status),x+s(375,dpi),yy,x+s(445,dpi),yy+rowH,RGB(90,102,120),small,DT_CENTER|DT_VCENTER|DT_SINGLELINE);wcopy3(buf,320,(WCHAR*)r->reusable_rule);wcat3(buf,320,L"  ｜教训：");wcat3(buf,320,(WCHAR*)r->lesson);text(dc,buf,x+s(455,dpi),yy+s(3,dpi),x+w-s(12,dpi),yy+rowH-s(3,dpi),RGB(65,78,98),small,DT_LEFT|DT_WORDBREAK|DT_END_ELLIPSIS);}
    if(n==0)text(dc,L"暂无经验。只有预测周期成熟、完成自动判卷和AI复盘，并通过质量门控后才会形成正式经验。",x+s(18,dpi),rowY+s(58,dpi),x+w-s(18,dpi),rowY+s(110,dpi),RGB(108,121,141),body,DT_LEFT|DT_VCENTER|DT_SINGLELINE);HeapFree(GetProcessHeap(),0,rows);
}

'''
marker = 'static void draw_placeholder(HDC dc,const LayoutInfo* L,HFONT body,HFONT bold,HFONT big)'
if 'static void draw_experience_page' not in s:
    s = s.replace(marker, func + marker)
s = s.replace('L"V0.6 已接入预测档案、自动判卷与AI复盘基础链路。成熟判卷会基于预测时冻结证据与真实结果生成结构化复盘。"', 'L"V0.7 已接入预测档案、自动判卷、AI复盘与经验库基础闭环。成熟复盘会经过质量门控生成可检索经验。"')
s = s.replace('L"当前主链：真实数据 → Snapshot → DeepSeek → 预测档案 → 自动判卷 → AI复盘。经验库仍需下一阶段质量门控后才会正式写入。"', 'L"当前主链：真实数据 → Snapshot → DeepSeek → 预测档案 → 自动判卷 → AI复盘 → 经验提取 → 下一次预测召回。"')
s = s.replace('else if(gPage==5)draw_review_page(dc,&L,small,body,bold,big);else if(gPage==9)', 'else if(gPage==5)draw_review_page(dc,&L,small,body,bold,big);else if(gPage==6)draw_experience_page(dc,&L,small,body,bold,big);else if(gPage==9)')
needle = 'storage_log_ex(&gStorage,L"INFO",L"AI_REVIEW",NULL,m);}if(!storage_save_funds'
repl = 'storage_log_ex(&gStorage,L"INFO",L"AI_REVIEW",NULL,m);}{int sr=0,cr=0,mg=0,rj=0;WCHAR m[220],n[24];experience_sync_reviews(&gStorage,&r->store,&sr,&cr,&mg,&rj);wcopy3(m,220,L"经验提取 scanned_reviews=");int_text(sr,n,24);wcat3(m,220,n);wcat3(m,220,L" created=");int_text(cr,n,24);wcat3(m,220,n);wcat3(m,220,L" merged=");int_text(mg,n,24);wcat3(m,220,n);wcat3(m,220,L" rejected=");int_text(rj,n,24);wcat3(m,220,n);storage_log_ex(&gStorage,L"INFO",L"EXPERIENCE_EXTRACT",NULL,m);}if(!storage_save_funds'
if needle in s:
    s = s.replace(needle, repl)
p.write_text(s, encoding='utf-8')

# Build script
p = root / 'build_windows.sh'
s = p.read_text(encoding='utf-8')
s = s.replace('for f in core storage network parser provider snapshot prediction_input prediction_repair grading archive review_logic review deepseek main; do', 'for f in core storage network parser provider snapshot prediction_input prediction_repair grading archive review_logic review experience deepseek main; do')
s = s.replace('"$BUILD/review.obj" "$BUILD/deepseek.obj"', '"$BUILD/review.obj" "$BUILD/experience.obj" "$BUILD/deepseek.obj"')
s = s.replace('/GS- /Zl', '/GS- /Gs65536 /Zl')
s = s.replace('AI基金预测_V0.6_AI复盘基础版_免安装.exe','AI基金预测_V0.7_AI经验闭环基础版_免安装.exe')
p.write_text(s, encoding='utf-8')

# README
(root / 'README.md').write_text('''# AI基金预测 V0.7 — AI经验闭环基础版

Windows x64 免安装版本。继续使用现有 `D:\\AI基金预测\\` 持久化数据。

V0.7 新增正式经验库 `data\\experience_store_v1.bin`。只有完成真实结果判卷与AI复盘并通过质量门控的复盘，才会形成可检索经验。经验会按 reusable_rule 去重合并并评分；预测前最多召回5条同基金或同基金类型的高质量经验。

质量门控拒绝 Snapshot 缺失、幸运命中、UNSUPPORTED、evidence_score<55、review_confidence<55、D级复盘。历史经验只作为参考，不能覆盖当前 Snapshot 事实。

Prompt 版本升级为2，因此 V0.7 第一次运行可能因 prompt_version_changed 重新预测一次。

关键日志：`EXPERIENCE_EXTRACT` / `EXPERIENCE_SAVE` / `EXPERIENCE_INJECT`。
''', encoding='utf-8')

print('V0.7 overlay applied to', root)
