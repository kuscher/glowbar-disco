package io.github.kuscher.disco

import android.app.Activity
import android.content.ActivityNotFoundException
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.widget.Toast

/** Opens Glowbar Disco, Glowbar's hidden party mode, and closes. Disco has no window of its own. */
class DiscoActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        try {
            // Glowbar's own task: tapping Disco again brings the same Disco window back instead of a second one.
            startActivity(Intent(Intent.ACTION_VIEW, Uri.parse("glowbar://disco")).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
        } catch (_: ActivityNotFoundException) {
            Toast.makeText(applicationContext, R.string.no_glowbar, Toast.LENGTH_LONG).show()
        }
        finish()
    }
}
