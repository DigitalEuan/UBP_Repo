package com.ubp.geometricos

import android.content.Context
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

/**
 * Python bridge for GeometricOS Version 2
 * 
 * Interfaces with full UBP 3.5 coherence-native system:
 * - 9 physical realms
 * - Geometric error correction
 * - Self-actualizing observer
 * - Coherence-aware caching
 */
class PythonBridge(private val context: Context) {
    
    private var python: Python? = null
    private var geometricosModule: com.chaquo.python.PyObject? = null
    
    suspend fun initialize() = withContext(Dispatchers.IO) {
        try {
            if (!Python.isStarted()) {
                Python.start(AndroidPlatform(context))
            }
            python = Python.getInstance()
            
            // Import geometricos_v2 module
            geometricosModule = python?.getModule("geometricos_v2")
            
            // Initialize the engine
            val cacheDir = context.cacheDir.absolutePath + "/ubp_cache"
            geometricosModule?.callAttr("initialize", cacheDir)
            
            true
        } catch (e: Exception) {
            e.printStackTrace()
            false
        }
    }
    
    suspend fun optimize(data: List<Double>, taskType: String = "general"): List<Double> = 
        withContext(Dispatchers.IO) {
            try {
                val result = geometricosModule?.callAttr("optimize", data, taskType)
                @Suppress("UNCHECKED_CAST")
                (result as? List<*>)?.map { (it as? Number)?.toDouble() ?: 0.0 } ?: data
            } catch (e: Exception) {
                e.printStackTrace()
                data
            }
        }
    
    suspend fun getStats(): Map<String, Any> = withContext(Dispatchers.IO) {
        try {
            val stats = geometricosModule?.callAttr("get_stats")
            convertPyObjectToMap(stats)
        } catch (e: Exception) {
            e.printStackTrace()
            emptyMap()
        }
    }
    
    suspend fun getRealms(): Map<String, Any> = withContext(Dispatchers.IO) {
        try {
            val realms = geometricosModule?.callAttr("get_realms")
            convertPyObjectToMap(realms)
        } catch (e: Exception) {
            e.printStackTrace()
            emptyMap()
        }
    }
    
    suspend fun enable() = withContext(Dispatchers.IO) {
        try {
            geometricosModule?.callAttr("enable")
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
    
    suspend fun disable() = withContext(Dispatchers.IO) {
        try {
            geometricosModule?.callAttr("disable")
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
    
    suspend fun clearCache() = withContext(Dispatchers.IO) {
        try {
            geometricosModule?.callAttr("clear_cache")
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
    
    @Suppress("UNCHECKED_CAST")
    private fun convertPyObjectToMap(pyObj: com.chaquo.python.PyObject?): Map<String, Any> {
        if (pyObj == null) return emptyMap()
        
        return try {
            val map = mutableMapOf<String, Any>()
            val keys = pyObj.callAttr("keys").asList()
            
            for (key in keys) {
                val keyStr = key.toString()
                val value = pyObj.callAttr("__getitem__", keyStr)
                
                map[keyStr] = when {
                    value == null -> ""
                    value.toString() == "True" -> true
                    value.toString() == "False" -> false
                    value.toString().toDoubleOrNull() != null -> value.toString().toDouble()
                    value.toString().toIntOrNull() != null -> value.toString().toInt()
                    // Check if it's a nested dict
                    try { value.callAttr("keys"); true } catch (e: Exception) { false } -> {
                        convertPyObjectToMap(value)
                    }
                    else -> value.toString()
                }
            }
            
            map
        } catch (e: Exception) {
            e.printStackTrace()
            emptyMap()
        }
    }
}
