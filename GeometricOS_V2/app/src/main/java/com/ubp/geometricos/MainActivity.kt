package com.ubp.geometricos

import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.animation.core.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {
    
    private lateinit var pythonBridge: PythonBridge
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        pythonBridge = PythonBridge(applicationContext)
        
        setContent {
            MaterialTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    GeometricOSV2Screen()
                }
            }
        }
    }
    
    @Composable
    fun GeometricOSV2Screen() {
        var isEnabled by remember { mutableStateOf(false) }
        var stats by remember { mutableStateOf<Map<String, Any>>(emptyMap()) }
        var realms by remember { mutableStateOf<Map<String, Any>>(emptyMap()) }
        val scope = rememberCoroutineScope()
        
        LaunchedEffect(Unit) {
            pythonBridge.initialize()
        }
        
        LaunchedEffect(isEnabled) {
            while (isEnabled) {
                stats = pythonBridge.getStats()
                realms = pythonBridge.getRealms()
                delay(2000)
            }
        }
        
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(24.dp)
                .verticalScroll(rememberScrollState()),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // Header
            Text(
                text = "GeometricOS",
                style = MaterialTheme.typography.headlineLarge,
                fontWeight = FontWeight.Bold
            )
            
            Text(
                text = "Version 2.0",
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.primary
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            Text(
                text = "UBP 3.5 Coherence-Native",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.secondary
            )
            
            Spacer(modifier = Modifier.height(32.dp))
            
            // Main Toggle
            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(
                    containerColor = if (isEnabled) 
                        MaterialTheme.colorScheme.primaryContainer 
                    else 
                        MaterialTheme.colorScheme.surfaceVariant
                )
            ) {
                Column(
                    modifier = Modifier.padding(24.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Switch(
                        checked = isEnabled,
                        onCheckedChange = { enabled ->
                            isEnabled = enabled
                            if (enabled) {
                                startService(Intent(this@MainActivity, OptimizationService::class.java))
                                scope.launch { pythonBridge.enable() }
                            } else {
                                stopService(Intent(this@MainActivity, OptimizationService::class.java))
                                scope.launch { pythonBridge.disable() }
                            }
                        },
                        modifier = Modifier.size(64.dp)
                    )
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    Text(
                        text = if (isEnabled) "ACTIVE" else "INACTIVE",
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold
                    )
                }
            }
            
            if (isEnabled && stats.isNotEmpty()) {
                Spacer(modifier = Modifier.height(24.dp))
                
                // Performance Card
                PerformanceCard(stats)
                
                Spacer(modifier = Modifier.height(16.dp))
                
                // Realm Usage Card
                RealmUsageCard(stats, realms)
                
                Spacer(modifier = Modifier.height(16.dp))
                
                // System Health Card
                SystemHealthCard(stats)
                
                Spacer(modifier = Modifier.height(16.dp))
                
                // Actions
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceEvenly
                ) {
                    Button(
                        onClick = { scope.launch { pythonBridge.clearCache() } }
                    ) {
                        Icon(Icons.Default.Delete, contentDescription = null)
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("Clear Cache")
                    }
                }
            }
        }
    }
    
    @Composable
    fun PerformanceCard(stats: Map<String, Any>) {
        Card(modifier = Modifier.fillMaxWidth()) {
            Column(modifier = Modifier.padding(16.dp)) {
                Row(
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(
                        Icons.Default.Speed,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.primary
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        "Performance",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold
                    )
                }
                
                Spacer(modifier = Modifier.height(12.dp))
                
                StatRow("Speedup", "${stats["speedup_percent"]}% ✓ Proven")
                StatRow("Quality (NRCI)", "${(stats["nrci"] as? Double)?.let { "%.10f".format(it) } ?: "N/A"}")
                StatRow("Operations", "${stats["total_operations"]}")
                StatRow("Cache Hit Rate", "${stats["cache_hit_rate"]}%")
            }
        }
    }
    
    @Composable
    fun RealmUsageCard(stats: Map<String, Any>, realms: Map<String, Any>) {
        Card(modifier = Modifier.fillMaxWidth()) {
            Column(modifier = Modifier.padding(16.dp)) {
                Row(
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(
                        Icons.Default.Hub,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.primary
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        "Active Realms",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold
                    )
                }
                
                Spacer(modifier = Modifier.height(12.dp))
                
                @Suppress("UNCHECKED_CAST")
                val realmUsage = stats["realm_usage"] as? Map<String, Any> ?: emptyMap()
                
                val realmIcons = mapOf(
                    "quantum" to "⚛️",
                    "electromagnetic" to "⚡",
                    "optical" to "🔬",
                    "gravitational" to "🌌",
                    "nuclear" to "☢️",
                    "biological" to "🧬",
                    "plasma" to "🔥",
                    "atomic" to "⚙️",
                    "cosmological" to "🌠"
                )
                
                for ((realm, pct) in realmUsage) {
                    val percentage = (pct as? Number)?.toDouble() ?: 0.0
                    if (percentage > 0.0) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            Text(
                                "${realmIcons[realm] ?: "•"} ${realm.replaceFirstChar { it.uppercase() }}",
                                style = MaterialTheme.typography.bodyMedium
                            )
                            Text(
                                "%.1f%%".format(percentage),
                                style = MaterialTheme.typography.bodyMedium,
                                fontWeight = FontWeight.Bold
                            )
                        }
                        Spacer(modifier = Modifier.height(4.dp))
                    }
                }
            }
        }
    }
    
    @Composable
    fun SystemHealthCard(stats: Map<String, Any>) {
        Card(modifier = Modifier.fillMaxWidth()) {
            Column(modifier = Modifier.padding(16.dp)) {
                Row(
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(
                        Icons.Default.HealthAndSafety,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.primary
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        "System Health",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold
                    )
                }
                
                Spacer(modifier = Modifier.height(12.dp))
                
                StatRow("Health", stats["system_health"]?.toString() ?: "Unknown")
                StatRow("Observer", if (stats["observer_converged"] == true) "Converged ✓" else "Converging...")
                StatRow("Coherence Restorations", "${stats["coherence_restorations"]}")
                StatRow("UBP Version", stats["ubp_version"]?.toString() ?: "3.5")
                StatRow("Architecture", stats["architecture"]?.toString() ?: "coherence-native")
                StatRow("Realms Available", "${stats["realms_available"]}")
            }
        }
    }
    
    @Composable
    fun StatRow(label: String, value: String) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text(
                label,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            Text(
                value,
                style = MaterialTheme.typography.bodyMedium,
                fontWeight = FontWeight.Medium
            )
        }
        Spacer(modifier = Modifier.height(4.dp))
    }
}
