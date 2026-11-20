"""Traegt die feste Signatur (kalorien.keystore) in android/app/build.gradle ein."""
p = "android/app/build.gradle"
s = open(p).read()
block = """    signingConfigs {
        debug {
            storeFile file("kalorien.keystore")
            storePassword System.getenv("KEYSTORE_PASSWORD")
            keyAlias "kalorien"
            keyPassword System.getenv("KEYSTORE_PASSWORD")
        }
    }
    buildTypes {"""
assert s.count("    buildTypes {") == 1, "buildTypes nicht eindeutig"
open(p, "w").write(s.replace("    buildTypes {", block, 1))
print("Signatur eingetragen")
