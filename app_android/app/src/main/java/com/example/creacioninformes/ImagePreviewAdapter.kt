package com.example.creacioninformes

import android.net.Uri
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageButton
import android.widget.ImageView
import androidx.recyclerview.widget.RecyclerView

class ImagePreviewAdapter(
    private val items: MutableList<Uri>
) : RecyclerView.Adapter<ImagePreviewAdapter.ViewHolder>() {

    inner class ViewHolder(view: View) :
        RecyclerView.ViewHolder(view) {

        val imgPreview: ImageButton = view.findViewById(R.id.imgPreview)
        val btnRemove: ImageView = view.findViewById(R.id.btnRemoveImagePreview)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val v = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_image_preview, parent, false)
        return ViewHolder(v)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val uri = items[position]

        holder.imgPreview.setImageURI(uri)

        holder.btnRemove.setOnClickListener {
            items.removeAt(position)
            notifyItemRemoved(position)
        }
    }

    override fun getItemCount(): Int = items.size
}
