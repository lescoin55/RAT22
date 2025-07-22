package com.test.ratbinding;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        TextView textView = new TextView(this);
        textView.setText("Test App for RAT Binding");
        textView.setTextSize(20);
        textView.setPadding(50, 50, 50, 50);
        
        setContentView(textView);
    }
}