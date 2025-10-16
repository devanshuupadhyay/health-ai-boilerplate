// frontend/types/patient.ts

// This interface represents the FHIR resource part of the data
export interface PatientFHIR {
  resourceType: 'Patient';
  name?: {
    family: string;
    given: string[];
  }[];
  gender?: 'male' | 'female' | 'other' | 'unknown';
  birthDate?: string;
}

// This interface represents the full API response for a single patient
export interface PatientAPIResponse {
  id: number;
  fhir_resource: PatientFHIR;
}