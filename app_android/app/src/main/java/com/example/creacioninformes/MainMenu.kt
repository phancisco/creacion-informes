package com.example.creacioninformes

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import android.content.Intent
import android.widget.Button
import android.widget.TextView

class MainMenu : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main_menu)

        val btnCreate = findViewById<Button>(R.id.CreateReport)
        val btnHistory = findViewById<Button>(R.id.HistoryReport)
        val textLogout = findViewById<TextView>(R.id.TextLogout)

        btnCreate.setOnClickListener {
            startActivity(Intent(this, CreacionInforme1::class.java))
        }

        btnHistory.setOnClickListener {
            startActivity(Intent(this, HistoryActivity::class.java))
        }

        textLogout.setOnClickListener {
            startActivity(Intent(this, MainActivity::class.java))
            finish()
        }
    }
}