/* ============================================================================
   login-modal.js — TrickySSC in-place login popup            TSSC-LOGINMODAL-V1.1
   ----------------------------------------------------------------------------
   Include ONCE on any page (before </body> is fine):

       <script type="module" src="/login-modal.js"></script>

   After that, none of these leave the page any more — a popup opens instead:

     • any link whose href points at login.html   (intercepted automatically;
       ?next=/path on that link is honoured after login)
     • any element carrying a  data-login  attribute
           <button data-login>Login</button>
           <a data-login="/mock-test.html?mock=7">Start</a>   ← go there after login
     • from JS:
           tsscLogin.open()      → Promise<user|null>  always shows the popup
           tsscLogin.require()   → Promise<user|null>  resolves at once if already
                                                        signed in, else shows popup
           tsscLogin.user()      → current Firebase user or null
           tsscLogin.logout()    → sign out + clear tssc_user

   On success the module writes localStorage.tssc_user exactly like login.html
   does, then fires   window 'tssc:login'   with  detail:{user, method, profile}.
   Pages that already use onAuthStateChanged update on their own; pages that
   built their UI once at load can listen for 'tssc:login' and re-render.
   Dismissing the popup resolves the promise with null (never rejects).

   Uses the SAME Firebase SDK version as the rest of the site (10.7.1). If the
   page has already initialised the default app, that app is reused.
   ========================================================================== */

import { initializeApp, getApps, getApp }
  from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getFirestore, doc, setDoc, getDoc, getDocs, collection, query, where, serverTimestamp }
  from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";
import { getAuth, signInWithPopup, GoogleAuthProvider, signInWithPhoneNumber,
         RecaptchaVerifier, updateProfile, signOut, onAuthStateChanged }
  from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";

const FIREBASE_CONFIG = {
  apiKey:"AIzaSyC4kjEYEZ6Zit9su9V5xpUhMd7vLhE90zA",
  authDomain:"trickyssc-17bb3.firebaseapp.com",
  projectId:"trickyssc-17bb3",
  storageBucket:"trickyssc-17bb3.firebasestorage.app",
  messagingSenderId:"450627057220",
  appId:"1:450627057220:web:366267bf437d94f20c6e11"
};

const app  = getApps().length ? getApp() : initializeApp(FIREBASE_CONFIG);
const db   = getFirestore(app);
const auth = getAuth(app);
const gProvider = new GoogleAuthProvider();

/* ───────────────────────── markup + styles ───────────────────────── */

const GOOGLE_SVG = '<svg width="20" height="20" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>';

const CSS = `
#tsscLoginModal{position:fixed;inset:0;z-index:2147483000;display:none;align-items:center;justify-content:center;padding:1rem;
  background:rgba(15,23,42,.62);backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);
  font-family:'Hind','Segoe UI',system-ui,sans-serif;color:#1A202C;box-sizing:border-box;}
#tsscLoginModal.tlm-show{display:flex;}
#tsscLoginModal *{box-sizing:border-box;}
.tlm-card{width:100%;max-width:420px;background:#fff;border-radius:22px;box-shadow:0 24px 70px rgba(0,0,0,.28);
  overflow:hidden;position:relative;animation:tlmPop .22s ease-out;max-height:calc(100vh - 2rem);overflow-y:auto;}
@keyframes tlmPop{from{transform:translateY(14px) scale(.97);opacity:0}to{transform:none;opacity:1}}
.tlm-head{padding:1.4rem 1.6rem 1.1rem;border-bottom:1px solid #E2E8F0;background:linear-gradient(135deg,#fff9f5,#fff);}
.tlm-brand{display:flex;align-items:center;gap:.5rem;margin-bottom:.5rem;}
.tlm-brand-icon{width:30px;height:30px;border-radius:9px;background:linear-gradient(135deg,#FF6B00,#FF8C38);display:flex;align-items:center;justify-content:center;font-size:.95rem;box-shadow:0 3px 12px rgba(255,107,0,.35);}
.tlm-brand-name{font-family:'Baloo 2','Rajdhani',sans-serif;font-weight:800;font-size:1.05rem;}
.tlm-title{font-family:'Baloo 2','Rajdhani',sans-serif;font-size:1.35rem;font-weight:800;line-height:1.2;}
.tlm-sub{font-size:.85rem;color:#64748B;margin-top:.15rem;}
.tlm-close{position:absolute;top:.8rem;right:.8rem;width:34px;height:34px;border:none;border-radius:50%;background:#F1F5F9;color:#64748B;
  font-size:1.15rem;line-height:1;cursor:pointer;display:flex;align-items:center;justify-content:center;}
.tlm-close:hover{background:#E2E8F0;color:#1A202C;}
.tlm-body{padding:1.2rem 1.6rem 1.5rem;}
.tlm-tabs{display:flex;background:#F1F5F9;border-radius:10px;padding:3px;margin-bottom:1.1rem;}
.tlm-tab{flex:1;padding:.55rem;border:none;border-radius:8px;font-family:'Rajdhani',sans-serif;font-size:.9rem;font-weight:700;cursor:pointer;background:transparent;color:#64748B;transition:all .2s;}
.tlm-tab.on{background:#fff;color:#1A202C;box-shadow:0 2px 8px rgba(0,0,0,.1);}
.tlm-sec{display:none;} .tlm-sec.on{display:block;}
.tlm-msg{display:none;padding:.7rem .9rem;border-radius:10px;font-size:.86rem;font-weight:600;font-family:'Rajdhani',sans-serif;margin-bottom:.9rem;line-height:1.4;}
.tlm-msg.err{display:block;background:#FEF2F2;border:1px solid #FECACA;color:#DC2626;}
.tlm-msg.ok{display:block;background:#F0FDF4;border:1px solid #BBF7D0;color:#16A34A;}
.tlm-gbtn{width:100%;display:flex;align-items:center;justify-content:center;gap:.7rem;background:#fff;border:2px solid #E2E8F0;border-radius:12px;
  padding:.85rem 1rem;font-family:'Rajdhani',sans-serif;font-size:1rem;font-weight:700;color:#1A202C;cursor:pointer;transition:all .2s;margin-bottom:.9rem;}
.tlm-gbtn:hover{border-color:#4285F4;box-shadow:0 4px 15px rgba(66,133,244,.15);}
.tlm-gbtn:disabled{opacity:.6;cursor:not-allowed;}
.tlm-hint{text-align:center;font-size:.8rem;color:#94A3B8;font-family:'Rajdhani',sans-serif;}
.tlm-label{display:block;font-family:'Rajdhani',sans-serif;font-size:.76rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#64748B;margin-bottom:.45rem;}
.tlm-phonewrap{display:flex;border:2px solid #E2E8F0;border-radius:12px;overflow:hidden;margin-bottom:1rem;transition:border-color .2s;}
.tlm-phonewrap:focus-within{border-color:#FF6B00;}
.tlm-cc{padding:0 .9rem;background:#F8FAFC;font-family:'Rajdhani',sans-serif;font-size:.95rem;font-weight:700;display:flex;align-items:center;border-right:2px solid #E2E8F0;}
.tlm-phonewrap input{flex:1;min-width:0;padding:.85rem 1rem;border:none;outline:none;font-family:inherit;font-size:1rem;background:#fff;color:#1A202C;}
.tlm-input{width:100%;background:#F8FAFC;border:2px solid #E2E8F0;border-radius:12px;padding:.85rem 1rem;font-family:inherit;font-size:.95rem;color:#1A202C;outline:none;margin-bottom:1rem;}
.tlm-input:focus{border-color:#FF6B00;}
.tlm-otp{font-size:1.3rem;text-align:center;letter-spacing:.4em;}
.tlm-cta{width:100%;padding:.95rem;border:none;border-radius:12px;font-family:'Rajdhani',sans-serif;font-size:1.05rem;font-weight:700;letter-spacing:.5px;cursor:pointer;
  background:linear-gradient(135deg,#FF6B00,#FF8C38);color:#fff;box-shadow:0 4px 20px rgba(255,107,0,.35);transition:all .2s;}
.tlm-cta:hover{transform:translateY(-1px);box-shadow:0 8px 28px rgba(255,107,0,.45);}
.tlm-cta:disabled{opacity:.6;cursor:not-allowed;transform:none;}
.tlm-center{text-align:center;margin-bottom:1rem;}
.tlm-center .big{font-size:1.5rem;margin-bottom:.3rem;}
.tlm-center .t{font-family:'Rajdhani',sans-serif;font-weight:700;}
.tlm-center .s{font-size:.8rem;color:#94A3B8;margin-top:.15rem;}
.tlm-resend{text-align:center;margin-top:.75rem;font-size:.82rem;color:#94A3B8;}
.tlm-resend a{color:#FF6B00;font-weight:700;cursor:pointer;}
.tlm-step{display:none;} .tlm-step.on{display:block;}
.tlm-foot{padding:0 1.6rem 1.1rem;text-align:center;font-size:.74rem;color:#94A3B8;font-family:'Rajdhani',sans-serif;}
@media(max-width:520px){
  #tsscLoginModal{padding:0;align-items:flex-end;}
  .tlm-card{max-width:100%;border-radius:20px 20px 0 0;max-height:92vh;animation:tlmUp .25s ease-out;}
  @keyframes tlmUp{from{transform:translateY(40px);opacity:0}to{transform:none;opacity:1}}
}
`;

const HTML = `
<div class="tlm-card" role="dialog" aria-modal="true" aria-labelledby="tlmTitle">
  <button class="tlm-close" id="tlmClose" aria-label="Close">×</button>
  <div class="tlm-head">
    <div class="tlm-brand"><div class="tlm-brand-icon">⚡</div><div class="tlm-brand-name">TrickySSC</div></div>
    <div class="tlm-title" id="tlmTitle">Login to continue 👋</div>
    <div class="tlm-sub" id="tlmSub">Sign in or create your free account — you'll stay right here.</div>
  </div>
  <div class="tlm-body">
    <div class="tlm-tabs">
      <button class="tlm-tab on" id="tlmTabG" type="button">🔵 Google</button>
      <button class="tlm-tab" id="tlmTabM" type="button">📱 Mobile OTP</button>
    </div>

    <div class="tlm-sec on" id="tlmSecG">
      <div class="tlm-msg" id="tlmMsgG"></div>
      <button class="tlm-gbtn" id="tlmGBtn" type="button">${GOOGLE_SVG} Continue with Google</button>
      <p class="tlm-hint">Sign in with your Google account · Free &amp; instant</p>
    </div>

    <div class="tlm-sec" id="tlmSecM">
      <div class="tlm-msg" id="tlmMsgM"></div>

      <div class="tlm-step on" id="tlmStepPhone">
        <label class="tlm-label">📱 Mobile Number</label>
        <div class="tlm-phonewrap">
          <div class="tlm-cc">🇮🇳 +91</div>
          <input type="tel" id="tlmPhone" maxlength="10" placeholder="10-digit mobile number" inputmode="numeric" autocomplete="tel-national">
        </div>
        <button class="tlm-cta" id="tlmSendBtn" type="button">Send OTP →</button>
        <div id="tlm-recaptcha" style="margin-top:.8rem;"></div>
      </div>

      <div class="tlm-step" id="tlmStepOtp">
        <div class="tlm-center"><div class="big">📨</div>
          <div class="t">OTP sent to <span id="tlmSentTo" style="color:#FF6B00;"></span></div>
          <div class="s">Enter the 6-digit code</div></div>
        <input type="tel" id="tlmCode" maxlength="6" placeholder="Enter 6-digit OTP" class="tlm-input tlm-otp" inputmode="numeric" autocomplete="one-time-code">
        <button class="tlm-cta" id="tlmVerifyBtn" type="button">Verify OTP →</button>
        <div class="tlm-resend">Didn't receive? <a id="tlmResend">Resend OTP</a></div>
      </div>

      <div class="tlm-step" id="tlmStepName">
        <div class="tlm-center"><div class="big">✅</div>
          <div class="t">Phone verified!</div>
          <div class="s">Just tell us your name</div></div>
        <label class="tlm-label">👤 Full Name</label>
        <input type="text" id="tlmName" placeholder="Enter your full name" class="tlm-input" autocomplete="name">
        <button class="tlm-cta" id="tlmDoneBtn" type="button">Start Learning →</button>
      </div>
    </div>
  </div>
  <div class="tlm-foot">Google and Mobile OTP are separate accounts — use the method you signed up with.</div>
</div>`;

/* ───────────────────────── state ───────────────────────── */

let root = null;               // #tsscLoginModal
let pending = null;            // { resolve, next, reload }
let confirmation = null;       // Firebase ConfirmationResult
let otpPhone = '';             // '+91XXXXXXXXXX'
let pendingUser = null;        // phone user waiting for a name
let verifier = null;           // RecaptchaVerifier
let tab = 'google';
let pendingPromise = null;
const $ = id => root.querySelector('#' + id);

/* ───────────────────────── helpers ───────────────────────── */

function safeNext(n){
  if(!n) return '';
  try{
    const u = new URL(n, location.href);
    if(u.origin !== location.origin) return '';
    return u.pathname + u.search + u.hash;
  }catch(_){ return ''; }
}
function isCurrentPage(path){
  try{ const u = new URL(path, location.href); return u.pathname === location.pathname && u.search === location.search; }
  catch(_){ return false; }
}
function msg(which, type, text){           // which: 'g' | 'm'
  const el = which === 'g' ? $('tlmMsgG') : $('tlmMsgM');
  if(!type || !text){ el.className = 'tlm-msg'; el.textContent = ''; return; }
  el.className = 'tlm-msg ' + (type === 'error' ? 'err' : 'ok');
  el.innerHTML = text;
}
function step(name){
  ['Phone','Otp','Name'].forEach(s => $('tlmStep' + s).classList.toggle('on', s === name));
}
function setTab(t){
  tab = t;
  $('tlmTabG').classList.toggle('on', t === 'google');
  $('tlmTabM').classList.toggle('on', t === 'mobile');
  $('tlmSecG').classList.toggle('on', t === 'google');
  $('tlmSecM').classList.toggle('on', t === 'mobile');
  if(t === 'mobile'){ initRecaptcha(); setTimeout(() => $('tlmPhone')?.focus(), 80); }
}
function normPhone(v){
  let d = String(v == null ? '' : v).replace(/\D/g, '');
  if(d.length === 12 && d.startsWith('91')) d = d.slice(2);
  if(d.length === 11 && d.startsWith('0'))  d = d.slice(1);
  return d.length === 10 ? d : '';
}
/* TSSC-PHONEUNIQ-V1 — same rule as login.html: one number, one account.
   Throws on failure so callers fail CLOSED. */
async function phoneOwner(ten, exceptUid){
  for(const form of ['+91' + ten, ten]){
    const snap = await getDocs(query(collection(db, 'users'), where('phone', '==', form)));
    for(const d of snap.docs) if(d.id !== exceptUid) return { uid: d.id, data: d.data() || {} };
  }
  return null;
}
async function saveGoogleProfile(user){
  const ref = doc(db, 'users', user.uid);
  const snap = await getDoc(ref);
  if(!snap.exists()){
    await setDoc(ref, {
      uid: user.uid, name: user.displayName || 'Student', email: user.email || '',
      phone: user.phoneNumber || '', photoURL: user.photoURL || '',
      createdAt: serverTimestamp(), loginMethod: 'google',
      totalTests: 0, avgScore: 0, bestScore: 0,
    });
  }
}
function initRecaptcha(){
  if(verifier) return;
  try{
    verifier = new RecaptchaVerifier(auth, 'tlm-recaptcha', { size: 'invisible', callback: () => {} });
  }catch(e){ console.warn('[login-modal] recaptcha init failed:', e.message); verifier = null; }
}
function clearRecaptcha(){
  try{ verifier && verifier.clear(); }catch(_){}
  verifier = null;
  const el = root && $('tlm-recaptcha'); if(el) el.innerHTML = '';
}
function resetForms(){
  msg('g'); msg('m');
  step('Phone');
  $('tlmPhone').value = ''; $('tlmCode').value = ''; $('tlmName').value = '';
  $('tlmSendBtn').disabled = false;  $('tlmSendBtn').textContent = 'Send OTP →';
  $('tlmVerifyBtn').disabled = false; $('tlmVerifyBtn').textContent = 'Verify OTP →';
  $('tlmDoneBtn').disabled = false;  $('tlmDoneBtn').textContent = 'Start Learning →';
  $('tlmGBtn').disabled = false;     $('tlmGBtn').innerHTML = GOOGLE_SVG + ' Continue with Google';
  confirmation = null; otpPhone = ''; pendingUser = null;
  clearRecaptcha();
}

/* ───────────────────────── finish / close ───────────────────────── */

function finish(user, method, profile){
  const data = {
    uid: user.uid,
    name: (profile && profile.name) || user.displayName || 'Student',
    phone: (profile && profile.phone) || user.phoneNumber || '',
    email: (profile && profile.email != null) ? profile.email : (user.email || ''),
    photoURL: user.photoURL || '',
    loginMethod: method,
  };
  localStorage.setItem('tssc_user', JSON.stringify(data));
  localStorage.removeItem('loginReturnTo');           // stale key from the old flow
  window.dispatchEvent(new CustomEvent('tssc:login', { detail: { user, method, profile: data } }));

  msg(tab === 'google' ? 'g' : 'm', 'success', '✅ Logged in! Taking you back…');
  const p = pending; pending = null;
  setTimeout(() => {
    close(true);
    if(p){
      p.resolve(user);
      if(p.next && !isCurrentPage(p.next)) location.href = p.next;
      else if(p.reload) location.reload();
    }
  }, 650);
}
function close(done){
  if(!root) return;
  root.classList.remove('tlm-show');
  document.documentElement.style.overflow = '';
  resetForms();
  if(!done && pending){ const p = pending; pending = null; p.resolve(null); }
}

/* ───────────────────────── flows ───────────────────────── */

async function googleLogin(){
  const btn = $('tlmGBtn');
  btn.disabled = true; btn.innerHTML = '⏳ Signing in…';
  msg('g');
  try{
    const result = await signInWithPopup(auth, gProvider);
    try{ await saveGoogleProfile(result.user); }
    catch(e){ console.error('[login-modal] profile write failed, continuing:', e); }
    finish(result.user, 'google');
  }catch(e){
    btn.disabled = false; btn.innerHTML = GOOGLE_SVG + ' Continue with Google';
    if(e.code === 'auth/popup-blocked') msg('g', 'error', '⚠️ Popup blocked. Please allow popups for trickyssc.com');
    else if(e.code === 'auth/popup-closed-by-user' || e.code === 'auth/cancelled-popup-request') msg('g');
    else msg('g', 'error', 'Login failed: ' + e.message);
  }
}

async function sendOTP(){
  const phone = normPhone($('tlmPhone').value);
  const btn = $('tlmSendBtn');
  if(!phone){ msg('m', 'error', '⚠️ Enter valid 10-digit mobile number'); return; }
  btn.disabled = true; btn.textContent = '⏳ Sending OTP…'; msg('m');
  try{
    initRecaptcha();
    if(!verifier) throw new Error('reCAPTCHA could not start. Please reload and try again.');
    confirmation = await signInWithPhoneNumber(auth, '+91' + phone, verifier);
    otpPhone = '+91' + phone;
    $('tlmSentTo').textContent = '+91 ' + phone;
    step('Otp');
    msg('m', 'success', '✅ OTP sent to +91 ' + phone);
    setTimeout(() => $('tlmCode')?.focus(), 100);
  }catch(e){
    btn.disabled = false; btn.textContent = 'Send OTP →';
    if(e.code === 'auth/too-many-requests') msg('m', 'error', '⚠️ Too many attempts. Try after some time.');
    else if(e.code === 'auth/invalid-phone-number') msg('m', 'error', '⚠️ Invalid phone number.');
    else msg('m', 'error', 'Error: ' + e.message);
    clearRecaptcha();
  }
}

async function verifyOTP(){
  const code = $('tlmCode').value.trim();
  const btn = $('tlmVerifyBtn');
  if(code.length !== 6){ msg('m', 'error', '⚠️ Enter the 6-digit OTP'); return; }
  if(!confirmation){ msg('m', 'error', '⚠️ Please request an OTP first.'); step('Phone'); return; }
  btn.disabled = true; btn.textContent = '⏳ Verifying…';
  try{
    const result = await confirmation.confirm(code);
    const user = result.user;
    let returning = false;
    try{
      const snap = await getDoc(doc(db, 'users', user.uid));
      if(snap.exists() && snap.data().name && snap.data().name !== 'Student'){
        returning = true;
        const ud = snap.data();
        if(!user.displayName){ try{ await updateProfile(user, { displayName: ud.name }); }catch(_){} }
        finish(user, 'phone', { name: ud.name, phone: otpPhone, email: ud.email || '' });
      }
    }catch(fsErr){ console.warn('[login-modal] Firestore check failed, treating as new user:', fsErr.message); }
    if(!returning){
      pendingUser = user;
      step('Name'); msg('m');
      setTimeout(() => $('tlmName')?.focus(), 100);
    }
  }catch(e){
    btn.disabled = false; btn.textContent = 'Verify OTP →';
    if(e.code === 'auth/invalid-verification-code') msg('m', 'error', '⚠️ Wrong OTP. Please check and try again.');
    else if(e.code === 'auth/code-expired') msg('m', 'error', '⚠️ OTP expired. Please request a new one.');
    else msg('m', 'error', 'Error: ' + e.message);
  }
}

async function completeMobile(){
  const name = $('tlmName').value.trim();
  const btn = $('tlmDoneBtn');
  const user = pendingUser;
  if(name.length < 2){ msg('m', 'error', '⚠️ Please enter your full name'); return; }
  if(!user){ msg('m', 'error', '⚠️ Session lost. Please request the OTP again.'); step('Phone'); return; }
  btn.disabled = true; btn.textContent = '⏳ Saving…';

  // One number, one account (TSSC-PHONEUNIQ-V1). Fail closed if the check can't run.
  try{
    const ten = normPhone(otpPhone || user.phoneNumber || '');
    const owner = ten ? await phoneOwner(ten, user.uid) : null;
    if(owner){
      msg('m', 'error', 'This mobile number is already registered with a <b>Google login</b>. '
        + 'Please switch to the Google tab and sign in there — everything you have, '
        + 'including any course you bought, is in that account.');
      btn.disabled = false; btn.textContent = 'Start Learning →';
      try{ await signOut(auth); }catch(_){}
      pendingUser = null;
      return;
    }
  }catch(e){
    console.error('[login-modal] phone uniqueness check failed:', e);
    msg('m', 'error', 'Could not verify your number just now. Please check your connection and try again.');
    btn.disabled = false; btn.textContent = 'Start Learning →';
    return;
  }

  try{
    await setDoc(doc(db, 'users', user.uid), {
      uid: user.uid, name, phone: otpPhone, email: '', photoURL: '',
      loginMethod: 'phone', createdAt: serverTimestamp(),
      totalTests: 0, avgScore: 0, bestScore: 0,
    }, { merge: true });
    try{ await updateProfile(user, { displayName: name }); }catch(_){}
    finish(user, 'phone', { name, phone: otpPhone, email: '' });
  }catch(e){
    btn.disabled = false; btn.textContent = 'Start Learning →';
    msg('m', 'error', 'Error: ' + e.message);
  }
}

function resendOTP(){
  step('Phone'); msg('m');
  $('tlmCode').value = '';
  $('tlmSendBtn').disabled = false; $('tlmSendBtn').textContent = 'Send OTP →';
  clearRecaptcha();
  setTimeout(initRecaptcha, 300);
}

/* ───────────────────────── mount / open ───────────────────────── */

function mount(){
  if(root) return;
  const style = document.createElement('style');
  style.id = 'tsscLoginModalCss'; style.textContent = CSS;
  document.head.appendChild(style);
  root = document.createElement('div');
  root.id = 'tsscLoginModal'; root.innerHTML = HTML;
  document.body.appendChild(root);

  $('tlmClose').onclick = () => close(false);
  root.addEventListener('click', e => { if(e.target === root) close(false); });
  document.addEventListener('keydown', e => { if(e.key === 'Escape' && root.classList.contains('tlm-show')) close(false); });
  $('tlmTabG').onclick = () => setTab('google');
  $('tlmTabM').onclick = () => setTab('mobile');
  $('tlmGBtn').onclick = googleLogin;
  $('tlmSendBtn').onclick = sendOTP;
  $('tlmVerifyBtn').onclick = verifyOTP;
  $('tlmDoneBtn').onclick = completeMobile;
  $('tlmResend').onclick = resendOTP;
  $('tlmPhone').oninput = e => { e.target.value = e.target.value.replace(/\D/g, '').slice(0, 10); };
  $('tlmCode').oninput  = e => { e.target.value = e.target.value.replace(/\D/g, '').slice(0, 6); };
  $('tlmPhone').onkeydown = e => { if(e.key === 'Enter') sendOTP(); };
  $('tlmCode').onkeydown  = e => { if(e.key === 'Enter') verifyOTP(); };
  $('tlmName').onkeydown  = e => { if(e.key === 'Enter') completeMobile(); };
}

/**
 * open({ next, reload, title, sub })
 *   next   — same-origin path to go to AFTER login (omit to stay on this page)
 *   reload — reload this page after login (for pages that only read login state at load)
 *   title / sub — override the popup heading text
 * Resolves with the Firebase user, or null if the popup is dismissed.
 */
function open(opts = {}){
  mount();
  if(pending) return pendingPromise;           // already open — reuse
  if(opts.title) $('tlmTitle').textContent = opts.title; else $('tlmTitle').textContent = 'Login to continue 👋';
  if(opts.sub)   $('tlmSub').textContent = opts.sub;     else $('tlmSub').textContent = "Sign in or create your free account — you'll stay right here.";
  resetForms(); setTab('google');
  root.classList.add('tlm-show');
  document.documentElement.style.overflow = 'hidden';
  pendingPromise = new Promise(resolve => { pending = { resolve, next: safeNext(opts.next), reload: !!opts.reload }; });
  return pendingPromise;
}

async function require(opts = {}){
  try{ if(auth.authStateReady) await auth.authStateReady(); }catch(_){}
  if(auth.currentUser) return auth.currentUser;
  return open(opts);
}

async function logout(){
  try{ await signOut(auth); }catch(_){}
  localStorage.removeItem('tssc_user');
  window.dispatchEvent(new CustomEvent('tssc:logout'));
}

/* ─────────── intercept every "go to login.html" link / data-login ─────────── */

/* Resolve where a login click wants to go, then act. The auth check is ASYNC on
   purpose: Firebase restores an existing session from IndexedDB a few hundred ms
   after page load, so auth.currentUser is briefly null even for a signed-in user.
   Checking it synchronously would flash the popup at a logged-in (paid) user who
   clicked a stale Login button in that window. preventDefault() still happens
   synchronously, so the old page navigation never fires either way. */
async function handleLoginClick(next){
  try{ if(auth.authStateReady) await auth.authStateReady(); }catch(_){}
  const n = safeNext(next);
  if(auth.currentUser){                       // already signed in — no popup, ever
    localStorage.removeItem('loginReturnTo');
    if(n && !isCurrentPage(n)) location.href = n;
    return;
  }
  open({ next: n });
}

document.addEventListener('click', e => {
  const el = e.target.closest('a[href],[data-login]');
  if(!el) return;
  if(e.metaKey || e.ctrlKey || e.shiftKey || el.target === '_blank') return;

  if(el.hasAttribute('data-login')){
    e.preventDefault(); e.stopPropagation();
    handleLoginClick(el.getAttribute('data-login') || el.getAttribute('data-next') || '');
    return;
  }
  const href = el.getAttribute('href') || '';
  if(!/(^|\/)login\.html(\?|#|$)/i.test(href)) return;
  e.preventDefault(); e.stopPropagation();
  let next = '';
  try{
    const u = new URL(href, location.href);
    next = u.searchParams.get('next') || u.searchParams.get('return') || u.searchParams.get('redirect') || '';
  }catch(_){}
  if(!next){
    const rt = localStorage.getItem('loginReturnTo');   // old flow's stashed target
    if(rt && !isCurrentPage(rt)) next = rt;
  }
  handleLoginClick(next);
}, true);

/* ─────────── auth state on <html> + self-healing tssc_user ───────────
   No-flicker nav: a page marks its Login chip data-auth="out" and its
   signed-in chip data-auth="in", with this CSS in <head>:
     [data-auth]{visibility:hidden}
     html.tssc-auth-in [data-auth="in"],html.tssc-auth-out [data-auth="out"]{visibility:visible}
   Neither is shown until Firebase has actually restored the session, so a
   signed-in student never sees "Login" flash for a moment.
   The same pass rewrites localStorage.tssc_user from the real session when it
   is missing or belongs to a different uid, so pages that read that cache
   never disagree with Firebase about who is signed in. Existing richer
   records (name from Firestore, phone, etc.) are left alone. */
function markAuth(user){
  const h = document.documentElement;
  h.classList.toggle('tssc-auth-in',  !!user);
  h.classList.toggle('tssc-auth-out', !user);
  if(!user) return;
  try{
    const cur = JSON.parse(localStorage.getItem('tssc_user') || 'null');
    if(cur && cur.uid === user.uid) return;
    const prov = (user.providerData || []).map(p => p && p.providerId);
    localStorage.setItem('tssc_user', JSON.stringify({
      uid: user.uid, name: user.displayName || 'Student', phone: user.phoneNumber || '',
      email: user.email || '', photoURL: user.photoURL || '',
      loginMethod: prov.includes('phone') ? 'phone' : 'google',
    }));
  }catch(_){}
}
onAuthStateChanged(auth, markAuth);

window.tsscLogin = { open, require, close: () => close(false), user: () => auth.currentUser, logout, auth };
