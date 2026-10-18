# python3 env.py narration.wav > env.js  -> const ENV=[...] normalised loudness at 30/s (smoothed), used by lipsync.js
import sys,subprocess,numpy as np,json
wav=sys.argv[1]
raw=subprocess.run(['ffmpeg','-v','quiet','-i',wav,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
x=np.frombuffer(raw,np.float32);hop=16000//30
n=len(x)//hop;rms=np.array([np.sqrt(np.mean(x[i*hop:(i+1)*hop+hop//2]**2)+1e-12) for i in range(n)])
rms=rms/np.percentile(rms,98);rms=np.clip(rms,0,1)
rms=np.where(rms<.05,0,rms)                                   # noise floor -> silence
k=np.array([.25,.5,.25]);rms=np.convolve(rms,k,'same')         # light smoothing
print('const ENV='+json.dumps([round(float(v),3) for v in rms])+';')
