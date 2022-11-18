==============
Text-to-speech
==============
The OdooPBX Agent has a built-in support for Google Text-to-speech API.

For documentation on Google TTS API follow this `link <https://cloud.google.com/text-to-speech>`__.

For customization see `asteriskmod.py <https://github.com/odoopbx/agent/blob/master/salt/agent/files/etc/extensions/modules/asteriskmod.py#L284>`__ salt module.

You must prepare your server where the Agent & Asterisk run as described below.

API Key
=======
Download the Google TTS API key and save it to ``/etc/google_tts_key.json`` file. 
Or you can save it in any place and configure ``tts_google_key_file``  in ``minion_local.conf``. 

You can find some instructions on how to download the key file `here <https://www.youtube.com/results?search_query=Get+API+Key+text-to-speech>`__.

Usage example
=============
Use ``asterisk.tts_create_sound`` function that accepts the following parameters:

* **result_file** - file name of the target sound file, plased in the result_file_folder directory (see below).
* **text** - text that should be sent to Google TTS API.
* **language** - text language, ‘en-US’ is the default value.
* **voice** - Voice to be used for the target sound, default is ‘en-US-Wavenet-A’.
* **pitch** - Pitch used for sound, default is 0.
* **speacking_rate** - Speacking rate used sound default is 1.
* **tts_key_file_path** - custom path to Google API file in .json format, default is /srv/odoopbx/google_key.json.
* **result_file_folder** - target directory where the target sound file will be placed. The default is /var/lib/asterisk/sounds.):

You can get language and voice values from the Google API test page (use Show JSON link button).