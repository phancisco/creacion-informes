package com.example.creacioninformes

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import android.content.Intent
import android.widget.Button

class FinishInforme : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_finish_informe)

        val buttonDelete = findViewById<Button>(R.id.ButtonDelete)
        val buttonEdit = findViewById<Button>(R.id.ButtonEdit)
        val buttonFinish = findViewById<Button>(R.id.ButtonFinish)

        buttonDelete.setOnClickListener {
            startActivity(Intent(this, NotificacionActivity::class.java))
        }

        buttonEdit.setOnClickListener {
            startActivity(Intent(this, CreacionInforme1::class.java))
        }

        buttonFinish.setOnClickListener {
            startActivity(Intent(this, MainMenu::class.java))
        }
    }
}
