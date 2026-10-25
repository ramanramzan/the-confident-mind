"""Generate an original seven-page, fillable boundary-script workbook."""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/guide/The-Clear-Boundaries-Script-Kit.pdf'
for n,f in [('Sans','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf'),('Serif','DejaVuSerif.ttf')]:
    pdfmetrics.registerFont(TTFont(n,'/usr/share/fonts/truetype/dejavu/'+f))
W,H=595.28,841.89;INK='#0B0B10';GOLD='#C9A227';PAPER='#FBF8F1';GRAY='#585858'
c=canvas.Canvas(str(OUT),pagesize=(W,H),pageCompression=1)
c.setTitle('The Clear Boundaries Script Kit | The Confident Mind');c.setAuthor('The Confident Mind')
c.setSubject('20 original scripts, pushback replies, and a personal boundary planner')
def text(x,y,s,size=10,font='Sans',color=INK):
    c.setFont(font,size);c.setFillColor(HexColor(color));c.drawString(x,y,s)
def para(s,x,y,w=483,size=10,color=INK):
    p=Paragraph(s,ParagraphStyle('p',fontName='Sans',fontSize=size,leading=size*1.5,textColor=HexColor(color)))
    _,h=p.wrap(w,H);p.drawOn(c,x,y-h);return y-h
def line(y,x=56,w=483,color='#D7CEBA'):
    c.setStrokeColor(HexColor(color));c.setLineWidth(.6);c.line(x,y,x+w,y)
def crown(x,y,sc=1):
    c.saveState();c.translate(x,y);c.scale(sc,sc);c.setFillColor(HexColor(GOLD))
    p=c.beginPath();p.moveTo(-17,24);p.lineTo(-10,0);p.lineTo(10,0);p.lineTo(17,24);p.lineTo(5,15);p.lineTo(0,33);p.lineTo(-5,15);p.close();c.drawPath(p,fill=1,stroke=0);c.rect(-10,-5,20,3,fill=1,stroke=0);c.restoreState()
def frame(page,label,title,sub):
    c.setFillColor(HexColor(PAPER));c.rect(0,0,W,H,fill=1,stroke=0);crown(67,H-57,.44)
    text(86,H-48,'THE CONFIDENT MIND',9,'Bold');line(H-69)
    text(56,H-103,label,9,'Bold',GOLD);text(56,H-139,title,26,'Serif');para(sub,56,H-160,size=10,color=GRAY)
    line(49);text(56,32,'THE CLEAR BOUNDARIES SCRIPT KIT',7.3,color=GRAY);text(W-92,32,f'{page} / 7',8,color=GRAY)
def field(name,label,y,height=49):
    text(56,y,label,9.5,'Bold')
    c.acroForm.textfield(name=name,tooltip=label,x=56,y=y-height-13,width=W-112,height=height,fontName='Helvetica',fontSize=10,textColor=HexColor(INK),fillColor=HexColor('#FFFFFF'),borderColor=HexColor('#C9C1B1'),borderWidth=.7,forceBorder=True,fieldFlags='multiline',maxlen=1500)
    return y-height-41
def script_card(num,title,words,note,y):
    text(56,y,f'{num:02}',11,'Bold',GOLD);text(87,y,title,11,'Bold')
    bottom=para('"'+words+'"',87,y-12,w=W-143,size=11)
    bottom=para(note,87,bottom-6,w=W-143,size=8.7,color=GRAY)
    assert bottom>60,(num,bottom)
    line(bottom-12);return bottom-38
def end():c.showPage()

# Cover.
c.setFillColor(HexColor(INK));c.rect(0,0,W,H,fill=1,stroke=0)
c.setStrokeColor(HexColor('#6E5A30'));c.rect(26,26,W-52,H-52,fill=0,stroke=1);crown(W/2,H-102,1.05)
c.setFillColor(HexColor(GOLD));c.setFont('Bold',11);c.drawCentredString(W/2,H-137,'THE CONFIDENT MIND')
c.setFont('Sans',9);c.drawCentredString(W/2,H-185,'PRACTICAL WORDS FOR EVERYDAY LIMITS')
for s,y,size,col in [('THE CLEAR',H-270,31,PAPER),('BOUNDARIES',H-326,42,GOLD),('SCRIPT KIT',H-378,35,PAPER)]:
    c.setFont('Serif',size);c.setFillColor(HexColor(col));c.drawCentredString(W/2,y,s)
line(H-415,112,W-224,GOLD)
para('Say it clearly.<br/>Keep it respectful.<br/>Let your answer stand.',80,H-447,w=W-160,size=15,color=PAPER)
text(72,216,'20 ORIGINAL SCRIPTS',10,'Bold',GOLD)
text(72,191,'Work / Family / Friends / Digital life',10,color=PAPER)
text(72,151,'PLUS: PUSHBACK REPLIES + A PERSONAL PLANNER',8.7,color=PAPER)
text(72,91,'7 PAGES  /  PRINTABLE + FILLABLE  /  FREE RESOURCE',8,color='#C6C1B5');end()

frame(2,'01 / PREPARE','Before you say the words','Choose a limit you can act on. A script helps you communicate; it cannot guarantee another person\'s reaction.')
y=para('<b>Four useful checks</b><br/>1. What can I realistically offer?<br/>2. Is there an existing agreement or responsibility to address?<br/>3. What information does the person need to plan?<br/>4. What will I do if the request is repeated?',56,626,size=10.5)
y=para('Use these examples as starting points. Give a genuine reason when it helps. Offer an alternative only if you mean it. At work, clarify priorities and responsibilities rather than ignoring instructions.',56,y-18,size=9.5,color=GRAY)-28
y=field('situation','The situation I want to address',y,43)
y=field('limit','What I can offer, and where my limit is',y,43)
y=field('responsibility','An agreement or responsibility I need to account for',y,43)
para('Start with an ordinary, safe situation. If you face threats, coercion, or retaliation, prioritize safety and seek support suited to your circumstances.',56,111,size=9,color=GRAY);end()

groups=[
('02 / WORK','Protect realistic commitments','Discuss timing, priorities, and ownership. Adapt these examples to your role and actual responsibilities.',[
('An extra task','I can take this on if we move the report to Monday. Which should take priority?','Make the tradeoff visible when a manager adds work.'),
('A rushed deadline','I can send the summary today. The full review needs until Thursday.','Separate what is possible now from what needs more time.'),
('A coworker\'s request','I can explain the process for ten minutes, but I cannot finish the task for you.','Offer limited help only when you have capacity.'),
('After-hours messages','I will review this at the start of my next workday.','Use for non-urgent requests when you are not on call.'),
('An interruption','I need to finish this first. Can we talk at 2:30?','Name a time you can actually honor.')]),
('03 / FAMILY','Stay warm and specific','A clear limit describes your availability or action. It does not require someone else to agree.',[
('A surprise visit','Today is not a good time to visit. Please check with me before coming over.','Be specific about the arrangement you need.'),
('Private questions','I am keeping that part of my life private. Let\'s talk about something else.','You can redirect without disclosing personal details.'),
('A request for money','I am not able to lend money. I hope you find another option.','Do not promise financial help you cannot provide.'),
('A long phone call','I have ten minutes to talk today, and then I need to go.','State the window before the call expands.'),
('An insulting conversation','I want to discuss this, but I will end the call if the insults continue.','Choose a follow-through that is safe and within your control.')]),
('04 / FRIENDS','Make your yes intentional','Declining one request does not have to become a verdict on the whole friendship.',[
('An invitation','Thank you for inviting me. I am sitting this one out.','A simple answer can be enough for an optional event.'),
('A repeated favor','I cannot give you a ride this week. Please make another plan.','Give a clear answer early enough to help them plan.'),
('An expensive outing','That plan is outside my budget. I would be up for a walk instead.','Offer a different plan only if you genuinely want it.'),
('A heavy conversation','I care about you. I do not have the attention this needs tonight.','Be honest about capacity rather than half-listening.'),
('Changing an agreement','I agreed to help, and changing that affects you. Can we discuss a revised plan?','Acknowledge the impact instead of presenting a broken promise as a boundary.')]),
('05 / DIGITAL LIFE','Keep messages clear','Include necessary context. Shorter is not automatically better when a decision needs explanation.',[
('An immediate reply','I have seen your message. I will respond tomorrow when I can give it proper attention.','Return when you say you will, or update the person.'),
('Being added to a group','I am leaving this group to reduce messages. Please contact me directly about essential plans.','Choose a communication channel that works for you.'),
('Sharing a photo','Please ask before posting photos of me. I do not want this one shared.','State the specific privacy preference.'),
('An argument by text','I do not want to keep debating this in messages. I can talk tomorrow at 6.','A planned pause includes a realistic return when appropriate.'),
('Online pressure','I am not comfortable sharing that information.','You do not need to supply private details to satisfy a stranger.')]),
]
num=1
for page,(label,title,sub,items) in enumerate(groups,start=3):
    frame(page,label,title,sub);y=626
    for title,words,note in items:
        y=script_card(num,title,words,note,y);num+=1
    end()
assert num==21

frame(7,'06 / FOLLOW THROUGH','When someone pushes back','Check new information. If the request has not changed, you do not need a fresh justification each time.')
responses=[('"It will only take five minutes."','"I still cannot take it on today."'),('"But you did it last time."','"I had different capacity then. My answer this time is no."'),('"If you cared, you would."','"I care about you, and I am not available for this request."'),('"Just make an exception."','"I have considered it, and I am keeping my answer."'),('"You already promised."','"You are right. I need to acknowledge that and discuss how to repair the impact."')]
y=626
for objection,answer in responses:
    y=para('<b>'+objection+'</b> '+answer,56,y,size=9.2)-13
y=field('my_words','My words for one upcoming conversation',y-5,47)
y=field('follow_through','My safe next step if the same request is repeated',y,47)
y=para('<b>Afterward:</b> What actually happened? Did new information change your responsibility? What would you keep or adjust next time?',56,y+3,size=9)-17
text(56,y,'SOURCES & SCOPE',8,'Bold',GOLD)
y=para('Original educational examples by The Confident Mind. General guidance on brief, respectful refusals and communicating personal limits informed this kit. It is not therapy or legal, financial, or employment advice. No script guarantees agreement or safety.',56,y-10,size=8.3,color=GRAY)
for label,url in [('CCI - How to Say No Assertively (Module 6)','https://www.cci.health.wa.gov.au/~/media/CCI/Consumer-Modules/Assert-Yourself/Assert-Yourself---06---How-to-Say-No-Assertively.pdf'),('Cleveland Clinic - How to Set Healthy Boundaries','https://health.clevelandclinic.org/how-to-set-boundaries')]:
    y-=14;text(56,y,label,8,color=GRAY);c.linkURL(url,(56,y-2,W-56,y+9),thickness=0)
y-=18;text(56,y,'Sources checked: 25 October 2026. More free guides:',7.8,color=GRAY)
y-=13;text(56,y,'ramanramzan.github.io/the-confident-mind/free-guide.html',7.8,color=GRAY)
c.linkURL('https://ramanramzan.github.io/the-confident-mind/free-guide.html',(56,y-2,W-56,y+9),thickness=0)
assert y>58,y
end();c.save();print(OUT)
