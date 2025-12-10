package com.example.creacioninformes

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import android.content.Intent
import android.widget.Button
class NotificacionActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_notificacion)

        val buttonConfirm = findViewById<Button>(R.id.ButtonConfirmFinish)

        buttonConfirm.setOnClickListener {
            startActivity(Intent(this, MainMenu::class.java))
        }
    }
}
