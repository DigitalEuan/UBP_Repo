pluginManagement {
    repositories {google()
        mavenCentral()
        gradlePluginPortal()
        // Add this line
        maven { url = uri("https://chaquo.com/maven") }
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
        maven { url = uri("https://chaquo.com/maven") }
    }
}

rootProject.name = "GeometricOS_V2"
include(":app")
