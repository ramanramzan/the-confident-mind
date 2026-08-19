const menuToggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.nav');

if (menuToggle && nav) {
  const navId = nav.id || 'site-nav';
  nav.id = navId;
  menuToggle.type = 'button';
  menuToggle.setAttribute('aria-controls', navId);
  menuToggle.setAttribute('aria-expanded', 'false');
  menuToggle.setAttribute('aria-label', 'Open navigation');

  const closeNav = () => {
    nav.classList.remove('open');
    menuToggle.setAttribute('aria-expanded', 'false');
    menuToggle.setAttribute('aria-label', 'Open navigation');
    menuToggle.textContent = '☰';
  };

  menuToggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    menuToggle.setAttribute('aria-expanded', String(open));
    menuToggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
    menuToggle.textContent = open ? '×' : '☰';
  });

  nav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeNav));

  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && nav.classList.contains('open')) {
      closeNav();
      menuToggle.focus();
    }
  });

  document.addEventListener('click', event => {
    if (!nav.classList.contains('open')) return;
    if (nav.contains(event.target) || menuToggle.contains(event.target)) return;
    closeNav();
  });
}

const quiz = document.querySelector('[data-confidence-quiz]');
if (quiz) {
  const questions = [
    { text: 'How do you react when someone disagrees with you?', key: 'selfTrust', answers: [['I immediately question myself.', 1], ['I listen, then decide what I actually think.', 3], ['I need them to understand me before I can move on.', 2], ['I stay calm even when they strongly disagree.', 4]] },
    { text: 'When you make a mistake, what happens next?', key: 'selfTrust', answers: [['I replay it and criticize myself for a long time.', 1], ['I learn from it, but sometimes stay stuck on it.', 2], ['I identify the lesson and adjust.', 4], ['I usually hide it so nobody sees weakness.', 2]] },
    { text: 'How often do you change your plans because someone might judge you?', key: 'approval', answers: [['Often. I hate disappointing people.', 1], ['Sometimes, especially with people close to me.', 2], ['Rarely. I consider feedback without living by it.', 4], ['Almost never, even when the feedback could help.', 3]] },
    { text: 'Someone says no to a request. What do you assume?', key: 'approval', answers: [['They probably do not value me.', 1], ['I wonder what I did wrong.', 2], ['Their answer is information, not a verdict on me.', 4], ['Nothing. I move on immediately.', 3]] },
    { text: 'How comfortable are you saying “no” without a long explanation?', key: 'boundaries', answers: [['Very uncomfortable.', 1], ['I can do it with people I trust.', 2], ['I can say it clearly and respectfully.', 4], ['I say no so often that I sometimes shut people out.', 3]] },
    { text: 'Someone repeatedly crosses a boundary you already explained. What do you do?', key: 'boundaries', answers: [['I keep explaining myself.', 1], ['I become frustrated but avoid consequences.', 2], ['I restate it once and change my level of access.', 4], ['I cut them off immediately without a conversation.', 3]] },
    { text: 'In a difficult conversation, how do you usually communicate?', key: 'communication', answers: [['I overexplain because I want to be understood.', 1], ['I become quiet and hope the issue disappears.', 2], ['I stay direct, calm, and specific.', 4], ['I become blunt so nobody can misunderstand me.', 3]] },
    { text: 'How often do you ask for reassurance after making a decision?', key: 'approval', answers: [['Constantly.', 1], ['More often than I want.', 2], ['Occasionally, when the decision is genuinely uncertain.', 3], ['Rarely. I can live with my own decisions.', 4]] },
    { text: 'When motivation disappears, what happens to your important habits?', key: 'discipline', answers: [['They stop.', 1], ['I do a smaller version sometimes.', 2], ['I use routines to keep going.', 4], ['I rely on pressure and panic to finish.', 2]] },
    { text: 'How well do your actions match the standards you say you have?', key: 'discipline', answers: [['Not very well yet.', 1], ['Some areas are strong, others are inconsistent.', 2], ['Usually well, and I correct myself quickly.', 4], ['Very well, even if I become too rigid.', 3]] },
    { text: 'When you enter a room where you know nobody, what do you do?', key: 'selfTrust', answers: [['Wait for someone else to make me feel welcome.', 1], ['Stay quiet until someone approaches.', 2], ['Introduce myself and start small conversations.', 4], ['Act confident even if I feel nervous.', 3]] },
    { text: 'Which statement feels most like you?', key: 'selfTrust', answers: [['I need people to like me to feel secure.', 1], ['I am becoming more comfortable with myself.', 2], ['I can respect myself without needing universal approval.', 4], ['I do not care what anyone thinks of me.', 3]] }
  ];

  const questionEl = quiz.querySelector('.question');
  const answersEl = quiz.querySelector('.answers');
  const countEl = quiz.querySelector('.question-count');
  const progressEl = quiz.querySelector('.progress-line i');
  const nextBtn = quiz.querySelector('.quiz-next');
  const introEl = quiz.querySelector('.test-intro');
  const resultEl = quiz.querySelector('.result');
  const activeEl = quiz.querySelector('.quiz-active');
  const scoreEl = quiz.querySelector('.score');
  const profileEl = quiz.querySelector('.profile-name');
  const resultMessage = quiz.querySelector('.result-message');
  const dimensionsEl = quiz.querySelector('.dimensions');
  const nextStepEl = quiz.querySelector('.next-step');
  const startBtn = quiz.querySelector('.start-quiz');
  let current = 0;
  let selected = null;
  let scores = { selfTrust: 0, approval: 0, boundaries: 0, communication: 0, discipline: 0 };

  const labels = { selfTrust: 'Self-Trust', approval: 'Approval Independence', boundaries: 'Boundaries', communication: 'Communication', discipline: 'Discipline' };
  const dimensionMax = { selfTrust: 16, approval: 12, boundaries: 8, communication: 4, discipline: 8 };

  function renderQuestion() {
    const q = questions[current];
    selected = null;
    questionEl.textContent = q.text;
    countEl.textContent = `QUESTION ${current + 1} / ${questions.length}`;
    progressEl.style.width = `${((current + 1) / questions.length) * 100}%`;
    nextBtn.disabled = true;
    answersEl.innerHTML = q.answers.map((answer, index) => `<button class="answer" type="button" data-answer="${index}">${answer[0]}</button>`).join('');
    answersEl.querySelectorAll('.answer').forEach(btn => btn.addEventListener('click', () => {
      answersEl.querySelectorAll('.answer').forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
      selected = Number(btn.dataset.answer);
      nextBtn.disabled = false;
    }));
  }

  function showResult() {
    const total = Object.values(scores).reduce((a, b) => a + b, 0);
    const score = Math.round((total / (questions.length * 4)) * 100);
    let profile = 'THE STEADY BUILDER';
    let message = 'You already have a useful foundation. Your next level is consistency: make your strongest behaviors easier to repeat under pressure.';
    if (score < 50) {
      profile = 'THE RESET';
      message = 'Your confidence is carrying too much weight from approval, hesitation, or inconsistent boundaries. Start small and build evidence that you can trust yourself.';
    } else if (score < 70) {
      profile = 'THE BUILDER';
      message = 'You have confidence in some situations but lose it when pressure, disagreement, or uncertainty rises. Your next move is to make your responses more deliberate.';
    } else if (score >= 85) {
      profile = 'THE GROUNDED MIND';
      message = 'You have a strong confidence system: self-trust, boundaries, communication, and discipline reinforce each other. Protect the system from ego and rigidity.';
    }

    const lowestKey = Object.keys(scores).reduce((lowest, key) => {
      const currentRatio = scores[key] / dimensionMax[key];
      const lowestRatio = scores[lowest] / dimensionMax[lowest];
      return currentRatio < lowestRatio ? key : lowest;
    }, Object.keys(scores)[0]);
    const nextSteps = {
      selfTrust: 'Make one small decision each day for the next seven days without asking anyone to validate it.',
      approval: 'Before seeking reassurance, pause and write down what you think is the right decision and why.',
      boundaries: 'Choose one recurring boundary and state it once, clearly, without overexplaining.',
      communication: 'In your next difficult conversation, use one clear sentence for what you need and one for why.',
      discipline: 'Choose one important habit and define a minimum version you will complete even when motivation is low.'
    };

    scoreEl.textContent = `${score}`;
    profileEl.textContent = profile;
    resultMessage.textContent = message;
    nextStepEl.textContent = nextSteps[lowestKey];
    dimensionsEl.innerHTML = Object.entries(scores).map(([key, value]) => {
      const pct = Math.round((value / dimensionMax[key]) * 100);
      return `<div class="dimension"><div class="dimension-head"><span>${labels[key]}</span><span>${pct}%</span></div><div class="dimension-track"><i style="width:${pct}%"></i></div></div>`;
    }).join('');
    activeEl.style.display = 'none';
    resultEl.style.display = 'block';
    if (introEl) introEl.style.display = 'none';
  }

  startBtn?.addEventListener('click', () => {
    startBtn.closest('.test-start')?.remove();
    activeEl.style.display = 'block';
    renderQuestion();
  });

  nextBtn?.addEventListener('click', () => {
    const q = questions[current];
    if (selected === null) return;
    scores[q.key] += q.answers[selected][1];
    current += 1;
    if (current >= questions.length) showResult(); else renderQuestion();
  });
}

const chips = document.querySelectorAll('[data-filter]');
const cards = document.querySelectorAll('[data-category]');
if (chips.length && cards.length) {
  chips.forEach(chip => chip.addEventListener('click', () => {
    chips.forEach(c => c.classList.remove('active'));
    chip.classList.add('active');
    const filter = chip.dataset.filter;
    cards.forEach(card => {
      card.style.display = filter === 'all' || card.dataset.category === filter ? '' : 'none';
    });
  }));
}
