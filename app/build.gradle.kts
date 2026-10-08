plugins {
    alias(libs.plugins.android.application)
}

android {
    namespace = "io.github.kuscher.disco"
    compileSdk = 37

    defaultConfig {
        applicationId = "io.github.kuscher.disco"
        // Glowbar Disco lives on Googlebooks, and every Googlebook runs Android 17.
        minSdk = 37
        targetSdk = 37
        versionCode = 1
        versionName = "1.0"
    }

    // Signing from ~/.config/disco (never committed). Absent -> unsigned release build.
    val keyDir = File(System.getProperty("user.home"), ".config/disco")
    val keyFile = File(keyDir, "keystore.jks")
    val keyPassFile = File(keyDir, "keystore.pass")
    signingConfigs {
        if (keyFile.exists() && keyPassFile.exists()) {
            create("release") {
                storeFile = keyFile
                val pw = keyPassFile.readText().trim()
                storePassword = pw
                keyAlias = "disco"
                keyPassword = pw
            }
        }
    }

    buildTypes {
        // Debug builds use the release key when it exists, so a test install can replace a release.
        debug {
            signingConfig = signingConfigs.findByName("release") ?: signingConfigs.getByName("debug")
        }
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"))
            signingConfig = signingConfigs.findByName("release")
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    packaging {
        resources.excludes += setOf("META-INF/*.version", "kotlin-tooling-metadata.json")
    }
}
