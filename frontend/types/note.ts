// frontend/types/note.ts
export interface Note {
  id: number;
  content: string;
  patient_id: number;
  summary?: string;
}