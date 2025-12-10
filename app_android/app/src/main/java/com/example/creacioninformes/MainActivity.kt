package com.example.creacioninformes

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import android.content.Intent
import android.widget.Button
import android.widget.EditText
import android.widget.Toast

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val inputRut = findViewById<EditText>(R.id.InputRut)
        val inputPass = findViewById<EditText>(R.id.InputPassword)
        val buttonLogin = findViewById<Button>(R.id.ButtonLogin)

        buttonLogin.setOnClickListener {

            val rut = inputRut.text.toString()
            val password = inputPass.text.toString()
            //TEMPORAL HASTA QUE HAYA UNA API
            if (rut == "test" && password == "test") {
                goToMainMenu()
            } else {
                Toast.makeText(this, "Usuario o contraseña incorrectos", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun goToMainMenu() {
        val intent = Intent(this, MainMenu::class.java)
        startActivity(intent)
        finish()
    }
}