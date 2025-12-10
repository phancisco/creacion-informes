package com.example.creacioninformes

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.widget.Button
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView

class ParametroActivity : AppCompatActivity() {

    private lateinit var recyclerPreview: RecyclerView
    private lateinit var previewAdapter: ImagePreviewAdapter

    private val selectedImages = mutableListOf<Uri>()

    // launcher SOLO UNA VEZ
    private val pickImageLauncher =
        registerForActivityResult(ActivityResultContracts.GetMultipleContents()) { uris ->
            if (uris.isNotEmpty()) {
                selectedImages.addAll(uris)
                previewAdapter.notifyDataSetChanged()
            }
        }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_parametro)

        // inicializa recycler
        recyclerPreview = findViewById(R.id.recyclerPreviewImages)

        // inicializa adapter
        previewAdapter = ImagePreviewAdapter(selectedImages)

        // configurar recycler horizontal
        recyclerPreview.layoutManager = LinearLayoutManager(
            this,
            LinearLayoutManager.HORIZONTAL,
            false
        )
        recyclerPreview.adapter = previewAdapter


        // BOTÓN ADJUNTAR
        findViewById<Button>(R.id.ButtonAdjuntarImages).setOnClickListener {
            pickImageLauncher.launch("image/*")
        }

        // BOTÓN SIGUIENTE
        findViewById<Button>(R.id.ButtonNextParametros).setOnClickListener {
            startActivity(Intent(this, FinishInforme::class.java))
        }
    }
}
