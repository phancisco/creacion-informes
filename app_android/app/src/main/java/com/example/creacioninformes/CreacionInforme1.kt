package com.example.creacioninformes

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import android.content.Intent
import android.widget.Button

class CreacionInforme1 : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_creacion_informe1)

        val btnNext = findViewById<Button>(R.id.ButtonNextCreacionInforme1)

        btnNext.setOnClickListener {
            val intent = Intent(this, ParametroActivity::class.java)
            startActivity(intent)
        }
    }
}