package io.github.kuscher.disco

import android.app.Activity
import android.content.ActivityNotFoundException
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.widget.Toast

/**
 * Opens Glowbar Disco, Glowbar's hidden party mode, and closes. This shortcut has no window of its own.
 * The icon's right-click menu has one more item (res/xml/shortcuts.xml): the privacy policy, in the browser.
 */
class DiscoActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val privacy = intent?.action == ACTION_PRIVACY
        try {
            // A task of its own: clicking Disco again brings the same Glowbar Disco window back instead of a second one.
            startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(if (privacy) PRIVACY_URL else DISCO)).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
        } catch (_: ActivityNotFoundException) {
            if (!privacy) Toast.makeText(applicationContext, R.string.no_glowbar, Toast.LENGTH_LONG).show()
        }
        finish()
    }

    private companion object {
        const val DISCO = "glowbar://disco"
        const val ACTION_PRIVACY = "io.github.kuscher.disco.action.PRIVACY"
        const val PRIVACY_URL = "https://googlebook.studio/privacy/glowbar-disco"
    }
}
