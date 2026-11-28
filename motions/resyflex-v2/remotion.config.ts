import {Config} from '@remotion/cli/config';
Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(95);
// Navigateur : Remotion télécharge le sien. Pour en imposer un (ex. environnement cloud), définir REMOTION_CHROME=/chemin/vers/chrome-headless-shell
if (process.env.REMOTION_CHROME) Config.setBrowserExecutable(process.env.REMOTION_CHROME);
