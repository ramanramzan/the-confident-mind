"""Build the six-page printable and fillable Self-Worth Starter Kit.

Requires reportlab. Run from any directory; the output is a repository asset.
"""
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/guide/The-Self-Worth-Starter-Kit.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)
for name, filename in [('Sans','DejaVuSans.ttf'),('SansBold','DejaVuSans-Bold.ttf'),('Serif','DejaVuSerif.ttf')]:
    pdfmetrics.registerFont(TTFont(name, '/usr/share/fonts/truetype/dejavu/' + filename))
W,H=595.28,841.89
INK='#0B0B10'; GOLD='#C9A227'; PAPER='#FBF8F1'; MUTED='#585858'
c=canvas.Canvas(str(OUT),pagesize=(W,H),pageCompression=1)
c.setTitle('The Self-Worth Starter Kit | The Confident Mind')
c.setAuthor('The Confident Mind')
c.setSubject('Six-page printable and fillable workbook for a fairer view of yourself')
c.setKeywords('self-worth, self-esteem, reflection, worksheet, The Confident Mind')

def text(x,y,s,size=10,font='Sans',color=INK):
    c.setFillColor(HexColor(color));c.setFont(font,size);c.drawString(x,y,s)
def para(s,x,y,width=483,size=10.5,color=INK,leading=None):
    p=Paragraph(s,ParagraphStyle('body',fontName='Sans',fontSize=size,leading=leading or size*1.55,textColor=HexColor(color)))
    _,height=p.wrap(width,H);p.drawOn(c,x,y-height);return y-height
def line(y,color='#D8D2C5',x1=56,x2=W-56):
    c.setStrokeColor(HexColor(color));c.setLineWidth(.6);c.line(x1,y,x2,y)
def crown(x,y,scale=1):
    c.saveState();c.translate(x,y);c.scale(scale,scale)
    p=c.beginPath();p.moveTo(0,0);p.lineTo(-15,23);p.lineTo(-5,15);p.lineTo(0,31);p.lineTo(5,15);p.lineTo(15,23);p.lineTo(11,0);p.close()
    c.setFillColor(HexColor(GOLD));c.drawPath(p,fill=1,stroke=0);c.rect(-11,-5,22,3,fill=1,stroke=0);c.restoreState()
def frame(page,section,title,subtitle):
    c.setFillColor(HexColor(PAPER));c.rect(0,0,W,H,fill=1,stroke=0)
    crown(67,H-58,.48);text(86,H-49,'THE CONFIDENT MIND',9,'SansBold')
    text(W-121,H-49,f'WORKSHEET {page-1:02}',8,color=MUTED);line(H-69)
    text(56,H-100,section.upper(),9,'SansBold',GOLD)
    text(56,H-137,title,25,'Serif')
    para(subtitle,56,H-157,size=10,color=MUTED)
    line(49);text(56,32,'THE SELF-WORTH STARTER KIT',7.5,color=MUTED)
    text(W-92,32,f'{page} / 6',8,color=MUTED)
def field(name,label,y,height=53,hint=None):
    text(56,y,label,10,'SansBold')
    if hint:
        para(hint,56,y-8,size=8.8,color=MUTED);y-=25
    c.acroForm.textfield(name=name,tooltip=label,x=56,y=y-13-height,width=W-112,height=height,
        fontName='Helvetica',fontSize=10,textColor=HexColor(INK),fillColor=HexColor('#FFFFFF'),
        borderColor=HexColor('#C9C1B1'),borderWidth=.7,borderStyle='solid',forceBorder=True,
        fieldFlags='multiline',maxlen=1600)
    return y-13-height-30
def example(s,y,height=72):
    c.setFillColor(HexColor('#F0EBDF'));c.roundRect(56,y-height,W-112,height,7,fill=1,stroke=0)
    para(s,70,y-11,width=W-140,size=9.2);return y-height-25
def end():c.showPage()

# 1. Cover: a restrained editorial design with a permanent crown and brand name.
c.setFillColor(HexColor(INK));c.rect(0,0,W,H,fill=1,stroke=0)
c.setStrokeColor(HexColor('#65552D'));c.setLineWidth(.7);c.rect(26,26,W-52,H-52,fill=0,stroke=1)
crown(W/2,H-104,1.12)
c.setFillColor(HexColor(GOLD));c.setFont('SansBold',11);c.drawCentredString(W/2,H-137,'THE CONFIDENT MIND')
c.setFont('Sans',9);c.drawCentredString(W/2,H-186,'A PRACTICAL REFLECTION WORKBOOK')
for s,y,size,col in [('THE',H-263,22,PAPER),('SELF-WORTH',H-321,43,GOLD),('STARTER KIT',H-374,34,PAPER)]:
    c.setFont('Serif',size);c.setFillColor(HexColor(col));c.drawCentredString(W/2,y,s)
line(H-413,GOLD,115,W-115)
para('Build a fairer view of yourself.<br/>One thought. One example. One small action.',90,H-441,width=W-180,size=13,color=PAPER,leading=21)
text(71,269,'NOTICE',9,'SansBold',GOLD);text(71,247,'Catch the judgment.',10,color=PAPER)
text(71,215,'QUESTION',9,'SansBold',GOLD);text(71,193,'Look for a fuller picture.',10,color=PAPER)
text(71,161,'PRACTICE',9,'SansBold',GOLD);text(71,139,'Choose one respectful action.',10,color=PAPER)
text(71,91,'6 PAGES  /  PRINTABLE + FILLABLE  /  START ANY DAY',8,color='#C5C1B8')
end()

# 2. A notice-and-name log.
frame(2,'01 / Notice','Catch the critical voice','Start with one ordinary moment. Describe it without turning it into a verdict on your worth.')
y=example('<b>Example:</b> I stumbled over an answer in a meeting. My thought was "I am bad at my job." A missed answer is an event; the global judgment is something I can examine.',626,76)
y=field('moment','What happened? Stick to what you observed.',y,55)
y=field('thought','What did you say to yourself?',y,55)
y=field('feeling','What did you feel, and what did you want to do?',y,55)
y=field('notice','What is one thing you want to understand more fairly?',y,55)
para('How to use this kit: fill it in on a device or print it. Try one exercise at a time. You can skip a prompt that feels unhelpful; this is reflection, not a score.',56,111,size=9,color=MUTED)
end()

# 3. Distinguish evidence from a sweeping conclusion.
frame(3,'02 / Reframe','Separate the fact from the verdict','A balanced response can acknowledge a mistake without making it your whole identity.')
y=example('<b>Fact:</b> I missed one deadline.<br/><b>Verdict:</b> I am unreliable at everything.<br/><b>Fuller view:</b> I missed this deadline. I can tell the person, repair what I can, and adjust my plan.',626,88)
y=field('fact','1. What is the specific fact?',y,49)
y=field('judgment','2. What larger judgment did you add?',y,49)
y=field('fuller_picture','3. What evidence or context makes the picture more complete?',y,61)
y=field('balanced_response','4. Write a fair response and one useful next step.',y,65)
para('Aim for accurate, not artificially positive. You do not have to excuse harm or deny difficulty to treat yourself with respect.',56,101,size=9,color=MUTED)
end()

# 4. Original evidence-log structure.
frame(4,'03 / Recognize','Keep a record of what counts','Include ordinary effort, care, learning, or repair. Achievement is not a condition for having worth.')
y=example('<b>Example:</b> I noticed I was overloaded and asked for a realistic deadline. That showed honesty and awareness of my limits - even though I still felt nervous.',626,74)
for name,label in [('handled','One situation I handled'),('quality','A quality I showed, with a concrete example'),('learned','Something I learned or repaired'),('overlooked','Something useful I usually overlook about myself')]:
    y=field(name,label,y,53)
para('Keep this page for a week. Add a specific example when you notice one. There is no required number and no need to turn it into another performance target.',56,110,size=9,color=MUTED)
end()

# 5. Receive praise and practice a small boundary.
frame(5,'04 / Practice','Let respect become an action','Try accepting one kind comment and expressing one manageable preference or limit.')
y=example('<b>Receiving praise:</b> "Thank you. I appreciate you noticing."<br/><b>Setting a small limit:</b> "I can help for twenty minutes, but I cannot take on the whole task."<br/>Use your own words, and only offer help you can genuinely give.',626,92)
y=field('compliment','A compliment or kind comment I usually dismiss',y,45)
y=field('accept','A response that lets me receive it without arguing',y,45)
y=field('boundary','A preference or boundary I want to communicate',y,50)
y=field('action_words','My exact words, and when I could use them',y,50)
para('Choose a safe, low-stakes situation. Existing responsibilities may need a discussion rather than a refusal. If stating a limit could expose you to threats or harm, seek support suited to your circumstances.',56,104,size=9,color=MUTED)
end()

# 6. Seven-day practice plus a concise, attributable reading list.
frame(6,'05 / Continue','Your seven-day practice','This is a schedule you can adapt, not a promise of change in seven days. Reuse the worksheets as needed.')
rows=[('DAY 1','Notice one critical thought. Use worksheet 01.'),('DAY 2','Separate an event from a judgment. Use worksheet 02.'),('DAY 3','Record one overlooked quality. Use worksheet 03.'),('DAY 4','Receive a kind comment without dismissing it.'),('DAY 5','Express one safe, realistic preference or limit.'),('DAY 6','Take one manageable step you have been avoiding.'),('DAY 7','Review what helped. Choose one practice to repeat.')]
y=626
for day,action in rows:
    text(56,y,day,8,'SansBold',GOLD);para(action,113,y+3,width=W-169,size=9.3);line(y-17);y-=34
y=field('week_review','What helped, and what will I repeat next week?',y-4,50)
text(56,y,'A NOTE ON SUPPORT',8,'SansBold',GOLD)
y=para('These original exercises are for personal development, not diagnosis or treatment. If self-criticism is persistent, distressing, or disrupting daily life, consider speaking with a qualified mental health professional.',56,y-10,size=8.7)
y-=20;text(56,y,'SOURCES & FURTHER READING',8,'SansBold',GOLD)
y=para('General guidance on examining negative self-beliefs, recognizing strengths, and taking manageable challenges informed this resource. The prompts and examples were written by The Confident Mind; no assessment has been validated for this kit.',56,y-10,size=8.4)
for label,url in [('NHS - Raising low self-esteem','https://www.nhs.uk/mental-health/self-help/tips-and-support/raise-low-self-esteem/'),('Centre for Clinical Interventions - Self-esteem resources','https://www.cci.health.wa.gov.au/Resources/Looking-After-Yourself/Self-Esteem')]:
    y-=14;text(56,y,label,8,'Sans',MUTED);c.linkURL(url,(56,y-2,W-56,y+10),relative=0,thickness=0)
y-=18;text(56,y,'Sources checked: 25 October 2026. Visit the free guides:',7.7,color=MUTED)
y-=13;text(56,y,'ramanramzan.github.io/the-confident-mind/free-guide.html',7.7,color=MUTED)
c.linkURL('https://ramanramzan.github.io/the-confident-mind/free-guide.html',(56,y-2,W-56,y+10),thickness=0)
end();c.save()
print(OUT)
